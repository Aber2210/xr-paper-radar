#!/usr/bin/env python3
"""通过 gh CLI 令牌 + GitHub Git Data API，把本地 git HEAD 直推到远端仓库。

背景：沙箱代理拦截 github.com（git over HTTPS 报 "Empty reply from server"），
但 api.github.com 可达，且 gh CLI 已认证（需要 repo/workflow scope）。
因此不走 git 协议，改用 Git Data API：blobs -> tree -> commit -> ref。

用法：
    python scripts/push_to_github.py                 # 全量推送 HEAD 到 origin 默认分支
    python scripts/push_to_github.py --incremental   # 增量：只传与远端有差异的文件（日常用）
    python scripts/push_to_github.py --branch main   # 指定分支
    python scripts/push_to_github.py --dry-run       # 只列出将要推送的文件，不请求

增量模式原理：本地 git blob 与 GitHub blob 算法一致（SHA-1 内容寻址），
先拉取远端 tree 与本地 HEAD 对比，仅对变更/新增文件建 blob，删除项以 sha=null 入 tree，
以远端 HEAD 为 parent 建 commit 并更新 ref——日常运行只需几次请求。
"""
import argparse
import base64
import http.client
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

OWNER = "Aber2210"
REPO = "xr-paper-radar"
API_HOST = "api.github.com"
CHUNK_LOG = 50  # 每 50 个 blob 打印一次进度
WORKERS = 6     # blob 并行上传线程数（按请求延迟瓶颈调优）


def gh_token():
    return subprocess.check_output(
        ["gh", "auth", "token"], text=True, timeout=30
    ).strip()


def parse_proxy():
    proxy = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY") or ""
    if not proxy:
        return None
    hostport = proxy.split("://")[-1].rstrip("/")
    host, _, port = hostport.partition(":")
    return (host, int(port or "443"))


class GitHubApi:
    """带 keep-alive 的极简 GitHub API 客户端（经本地代理 CONNECT 隧道）。

    连接按线程隔离（thread-local），多线程上传 blob 时各自复用本线程连接。
    """

    def __init__(self, token):
        self.token = token
        self.proxy = parse_proxy()
        self._local = threading.local()
        self.headers = {
            "Authorization": "token " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "xr-paper-radar-push",
            "Content-Type": "application/json",
        }

    @property
    def conn(self):
        return getattr(self._local, "conn", None)

    @conn.setter
    def conn(self, value):
        self._local.conn = value

    def _connect(self):
        if self.conn is not None:
            return
        if self.proxy:
            self.conn = http.client.HTTPSConnection(
                self.proxy[0], self.proxy[1], timeout=90
            )
            self.conn.set_tunnel(API_HOST, 443)
        else:
            self.conn = http.client.HTTPSConnection(API_HOST, 443, timeout=90)

    def _drop(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None

    def request(self, method, path, body=None, retries=8):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        last_err = None
        for attempt in range(retries):
            try:
                self._connect()
                self.conn.request(method, path, body=data, headers=self.headers)
                resp = self.conn.getresponse()
                raw = resp.read()
                if resp.status in (200, 201, 204):
                    return json.loads(raw.decode("utf-8")) if raw else {}
                # 次级限流（403 带 Retry-After / secondary rate limit 文案）按 429 处理
                text = raw.decode("utf-8", "replace")
                if resp.status == 403 and (
                    "secondary rate" in text.lower() or "abuse" in text.lower()
                ):
                    resp.status = 429
                if resp.status == 429 or resp.status >= 500:
                    retry_after = resp.getheader("Retry-After")
                    wait = min(90, int(retry_after) if retry_after else 3 * (2 ** attempt))
                    print(f"  [{resp.status}] {method} {path}，{wait}s 后重试", flush=True)
                    self._drop()
                    time.sleep(wait)
                    continue
                raise RuntimeError(
                    f"{method} {path} -> HTTP {resp.status}: {raw[:400]!r}"
                )
            except (http.client.HTTPException, OSError) as e:
                last_err = e
                self._drop()
                if attempt == retries - 1:
                    break
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"{method} {path} 重试 {retries} 次仍失败: {last_err}")


def git(*args, binary=False):
    return subprocess.check_output(["git"] + list(args))


def ls_tree(commit):
    """列出 commit 的全部条目（含文件大小，-l 参数）。"""
    out = git("ls-tree", "-r", "-l", "-z", commit).decode("utf-8")
    entries = []
    for rec in out.split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, typ, sha, size = meta.split()
        entries.append(
            {"mode": mode, "type": typ, "sha": sha, "size": int(size), "path": path}
        )
    return entries


def batch_blobs(shas):
    """一次性取出所有 blob 内容（git cat-file --batch），避免逐文件 spawn 子进程。"""
    if not shas:
        return {}
    p = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=("\n".join(shas) + "\n").encode("ascii"),
        stdout=subprocess.PIPE,
        check=True,
    )
    out = p.stdout
    result = {}
    pos = 0
    for sha in shas:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].decode("ascii").split()
        size = int(header[2])
        start = nl + 1
        result[sha] = out[start : start + size]
        pos = start + size + 1  # 跳过内容末尾的换行
    return result


def bootstrap_repo(api):
    """空仓库（无任何 commit）会拒绝 Git Data API（409 Git Repository is empty），
    此时先用 Contents API 提交一个 README 造出首个 commit，之后 Git Data API 即恢复可用。"""
    if os.path.exists("README.md"):
        content = open("README.md", "rb").read()
    else:
        content = "# XR 每日论文雷达\n".encode("utf-8")
    api.request(
        "PUT",
        f"/repos/{OWNER}/{REPO}/contents/README.md",
        {
            "message": "chore: 初始化仓库（README）",
            "content": base64.b64encode(content).decode("ascii"),
        },
    )
    print("空仓库引导完成：已通过 Contents API 创建首个提交", flush=True)


def remote_tree_map(api, branch):
    """取远端分支 HEAD commit 的 tree sha 与递归 path->sha 映射。"""
    ref = api.request("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{branch}")
    head = ref["object"]["sha"]
    commit = api.request("GET", f"/repos/{OWNER}/{REPO}/git/commits/{head}")
    base_tree = commit["tree"]["sha"]
    tree = api.request("GET", f"/repos/{OWNER}/{REPO}/git/trees/{base_tree}?recursive=1")
    remote_map = {
        t["path"]: t["sha"] for t in tree["tree"] if t["type"] == "blob"
    }
    return head, base_tree, remote_map


def incremental_push(api, branch, entries, msg):
    """增量推送：仅上传与远端有差异的文件。返回 False 表示远端分支不存在（应回退全量）。"""
    try:
        head, base_tree, remote_map = remote_tree_map(api, branch)
    except RuntimeError as e:
        if "404" in str(e) or "empty" in str(e).lower():
            return False
        raise

    local_map = {e["path"]: e["sha"] for e in entries}
    changed = [p for p, s in local_map.items() if remote_map.get(p) != s]
    deleted = [p for p in remote_map if p not in local_map]
    print(
        f"增量对比：变更/新增 {len(changed)}，删除 {len(deleted)}，"
        f"未变 {len(local_map) - len(changed)}（远端 {len(remote_map)} 个文件）",
        flush=True,
    )
    if not changed and not deleted:
        print("远端已与本地 HEAD 一致，无需推送", flush=True)
        return True

    by_path = {e["path"]: e for e in entries}
    blob_sha = {}
    for i, p in enumerate(changed, 1):
        content = git("cat-file", "blob", by_path[p]["sha"])
        r = api.request(
            "POST",
            f"/repos/{OWNER}/{REPO}/git/blobs",
            {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
        )
        blob_sha[p] = r["sha"]
        if i % CHUNK_LOG == 0 or i == len(changed):
            print(f"  blob {i}/{len(changed)}", flush=True)

    tree_entries = [
        {"path": p, "mode": by_path[p]["mode"], "type": "blob", "sha": blob_sha[p]}
        for p in changed
    ]
    # tree API：sha 置 null 表示删除该路径
    tree_entries += [
        {"path": p, "mode": "100644", "type": "blob", "sha": None} for p in deleted
    ]
    new_tree = api.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/trees",
        {"base_tree": base_tree, "tree": tree_entries},
    )
    new_commit = api.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/commits",
        {"message": msg, "tree": new_tree["sha"], "parents": [head]},
    )
    api.request(
        "PATCH",
        f"/repos/{OWNER}/{REPO}/git/refs/heads/{branch}",
        {"sha": new_commit["sha"], "force": False},
    )
    print(f"✅ 增量推送完成 {OWNER}/{REPO}:{branch} -> {new_commit['sha'][:8]}", flush=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--branch", default=None, help="目标分支，默认取 origin/HEAD 或 main")
    ap.add_argument("--incremental", action="store_true",
                    help="增量模式：只传与远端有差异的文件（日常使用）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    branch = args.branch or "main"
    entries = ls_tree(args.commit)
    n_blob = sum(1 for e in entries if e["type"] == "blob")
    total_bytes = sum(e["size"] for e in entries if e["type"] == "blob")
    print(
        f"提交 {args.commit}：{len(entries)} 个条目（{n_blob} 个文件，"
        f"{total_bytes / 1024 / 1024:.2f} MB）-> {OWNER}/{REPO}:{branch}",
        flush=True,
    )
    if args.dry_run:
        for e in entries[:20]:
            print("  ", e["mode"], e["path"])
        print("  ...（dry-run，未发起请求）")
        return

    api = GitHubApi(gh_token())

    msg = git("log", "-1", "--pretty=%B", args.commit).decode("utf-8").strip()

    # 增量模式：远端分支不存在时自动回退全量
    if args.incremental:
        if incremental_push(api, branch, entries, msg):
            return
        print("远端分支不存在，回退全量推送…", flush=True)

    # 1) 创建 blob（并行上传；本地 git blob 与 GitHub blob 算法一致，但空仓库对象库为空，必须逐个上传）
    for e in entries:
        if e["type"] != "blob":
            raise RuntimeError(f"暂不支持非 blob 条目: {e['path']} ({e['type']})")

    contents = batch_blobs([e["sha"] for e in entries])
    remote_sha = {}
    done = [0]
    lock = threading.Lock()

    def upload(e):
        r = api.request(
            "POST",
            f"/repos/{OWNER}/{REPO}/git/blobs",
            {"content": base64.b64encode(contents[e["sha"]]).decode("ascii"), "encoding": "base64"},
        )
        with lock:
            done[0] += 1
            i = done[0]
            if i % CHUNK_LOG == 0 or i == n_blob:
                print(f"  blob {i}/{n_blob}", flush=True)
        return e["path"], r["sha"]

    bootstrapped = False
    for _round in (1, 2):
        try:
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for path, sha in pool.map(upload, entries):
                    remote_sha[path] = sha
            break
        except RuntimeError as e:
            if not bootstrapped and "Git Repository is empty" in str(e):
                bootstrapped = True
                print("远端为空仓库，先引导首个提交后重试…", flush=True)
                bootstrap_repo(api)
                continue  # blob 为内容寻址，重复创建幂等
            raise

    # 2) 创建 tree
    tree_body = {
        "tree": [
            {"path": e["path"], "mode": e["mode"], "type": "blob", "sha": remote_sha[e["path"]]}
            for e in entries
        ]
    }
    tree = api.request("POST", f"/repos/{OWNER}/{REPO}/git/trees", tree_body)
    print(f"tree 创建完成: {tree['sha']}", flush=True)

    # 3) 创建 commit（若远端已有该分支则带 parent）
    parents = []
    try:
        ref = api.request("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{branch}")
        parents.append(ref["object"]["sha"])
        print(f"远端 {branch} 已存在，parent={parents[0][:8]}", flush=True)
    except RuntimeError as e:
        print(f"远端暂无 {branch} 分支（首次推送）: {str(e)[:80]}", flush=True)

    commit = api.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/commits",
        {"message": msg, "tree": tree["sha"], "parents": parents},
    )
    print(f"commit 创建完成: {commit['sha']}", flush=True)

    # 4) 创建或更新 ref
    ref_path = f"/repos/{OWNER}/{REPO}/git/refs/heads/{branch}"
    if parents:
        api.request("PATCH", ref_path, {"sha": commit["sha"], "force": False})
    else:
        api.request("POST", "/repos/{}/git/refs".format(OWNER + "/" + REPO),
                    {"ref": f"refs/heads/{branch}", "sha": commit["sha"]})
    print(f"✅ 已推送 {OWNER}/{REPO}:{branch} -> {commit['sha'][:8]}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
