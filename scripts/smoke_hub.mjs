// CDP smoke test for web/xr-paper-hub.html (Edge headless)
// Usage: node smoke_hub.mjs <port> [project-root]
//
// 断言口径（2026-11-17 整改）：只断言「不变量」，不再钉死单批计数。
// 旧实现写死 papers===951 与 50+ 条 hasXXXXX，换批必须手改：
// 漏改 → 假 FAIL（把好批次判坏）；改错 → 假 PASS（把错计数写进期望值）。
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const port = Number(process.argv[2] || 9333);
const root = process.argv[3] || 'D:/Agent/WorkBuddy/Research';
const edge = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const target = 'file:///' + path.join(root, 'web/xr-paper-hub.html').replace(/\\/g, '/');
// profile 必须放 D 盘且用完即删：旧实现建在 os.tmpdir()（C 盘）且从不清理，
// 每次运行约 300–400 MB，累积多批后把 C 盘写满（2026-11-17 实测仅剩 0 字节）。
const TMP_ROOT = 'D:/Agent/.tmp';
fs.mkdirSync(TMP_ROOT, { recursive: true });
const profile = path.join(TMP_ROOT, 'edge-smoke-' + port);

const proc = spawn(edge, [
  '--headless=new', `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`, '--no-first-run', '--disable-gpu', target,
], { stdio: 'ignore' });

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// 统一收尾：杀 Edge 后把 profile 目录删掉。Edge 释放句柄有延迟，故带重试；
// 删除失败只在末尾告警，不改变断言语义。
async function finish(code) {
  try { proc.kill(); } catch { /* 已退出 */ }
  let removed = false;
  for (let i = 0; i < 20 && !removed; i++) {
    await sleep(150);
    try {
      fs.rmSync(profile, { recursive: true, force: true });
      removed = true;
    } catch { /* Edge 还没释放句柄，重试 */ }
  }
  if (!removed) console.error('WARN: 未能删除 profile 目录，请手工清理', profile);
  process.exit(code);
}

async function main() {
  // wait for devtools
  let ws = null;
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/list`);
      const tabs = await res.json();
      const page = tabs.find(t => t.type === 'page' && t.url.includes('xr-paper-hub'));
      if (page) { ws = page.webSocketDebuggerUrl; break; }
    } catch {}
    await sleep(250);
  }
  if (!ws) { console.error('FAIL: no devtools page target'); process.exit(1); }

  const WebSocket = (await import('node:worker_threads'), globalThis.WebSocket);
  const sock = new WebSocket(ws);
  await new Promise((res, rej) => { sock.onopen = res; sock.onerror = rej; });

  let id = 0;
  const pending = new Map();
  const errors = [];
  sock.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { res, rej } = pending.get(msg.id);
      pending.delete(msg.id);
      // exceptionDetails may be top-level (see project memory)
      if (msg.error) rej(new Error(JSON.stringify(msg.error)));
      else if (msg.result && msg.result.exceptionDetails) rej(new Error(JSON.stringify(msg.result.exceptionDetails)));
      else res(msg.result);
    } else if (msg.method === 'Runtime.exceptionThrown') {
      errors.push(msg.params.exceptionDetails.text + ' ' +
        (msg.params.exceptionDetails.exception?.description || ''));
    } else if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
      errors.push('console.error: ' + msg.params.args.map(a => a.value ?? a.description ?? '').join(' '));
    }
  };
  const send = (method, params = {}) => new Promise((res, rej) => {
    const mid = ++id;
    pending.set(mid, { res, rej });
    sock.send(JSON.stringify({ id: mid, method, params }));
  });

  await send('Runtime.enable');
  await send('Page.enable');
  await sleep(2500); // let page settle

  // 磁盘口径：这是唯一不能被「改期望值」篡改的基准
  const countLines = (p) => fs.readFileSync(p, 'utf8').split('\n').filter(l => l.trim()).length;
  const countMd = (d) => fs.readdirSync(d).filter(f => f.endsWith('.md')).length;
  const countDirs = (d) => fs.readdirSync(d, { withFileTypes: true }).filter(x => x.isDirectory()).length;
  const disk = {
    papers: countLines(path.join(root, 'papers/library/registry.jsonl')),
    notes: countMd(path.join(root, 'papers/notes')),
    batches: countDirs(path.join(root, 'papers/daily')),
  };

  const probe = await send('Runtime.evaluate', {
    expression: `(() => {
      const d = (typeof DATA !== 'undefined') ? DATA : null;
      const tabs = ['overview', 'daily', 'library', 'dim7', 'notes'];
      const rendered = {};
      for (const t of tabs) {
        const btn = document.querySelector('nav.tabs button[data-tab="' + t + '"]');
        if (!btn) { rendered[t] = -1; continue; }
        btn.click();
        const sec = document.getElementById('tab-' + t);
        rendered[t] = sec ? sec.children.length : -1;
      }
      const back = document.querySelector('nav.tabs button[data-tab="overview"]');
      if (back) back.click();
      const days = d ? d.batches.filter(b => /^\\d{4}-/.test(b.key)).map(b => b.key).sort().reverse().slice(0, 3) : [];
      return JSON.stringify({
        hasData: !!d,
        papers: d ? d.papers.length : -1,
        notes: d ? d.notes.length : -1,
        batches: d ? d.batches.length : -1,
        lastThree: days,
        lastThreePresent: d ? days.every(k => d.batches.some(b => b.key === k && Array.isArray(b.papers))) : false,
        allTitled: d ? d.papers.every(p => p.id && p.title_zh) : false,
        bodyLen: document.body ? document.body.innerHTML.length : -1,
        rendered: rendered
      });
    })()`,
    returnByValue: true, awaitPromise: false,
  });
  const info = JSON.parse(probe.result.value);
  console.log('PROBE:', JSON.stringify(info, null, 1));
  console.log('DISK:', JSON.stringify(disk));
  console.log('PAGE_ERRORS:', errors.length ? errors.join('\\n') : 'none');

  const checks = {
    hasData: info.hasData,
    papersEqDisk: info.papers === disk.papers,
    notesEqDisk: info.notes === disk.notes,
    batchesEqDisk: info.batches === disk.batches,
    lastThreePresent: info.lastThreePresent,
    allTitled: info.allTitled,
    tabsRender: Object.values(info.rendered).every(n => n > 0),
    noPageErrors: errors.length === 0,
    bodyLen: info.bodyLen > 10000,
  };
  console.log('CHECKS:', JSON.stringify(checks));
  const ok = Object.values(checks).every(Boolean);
  console.log(ok ? 'SMOKE: PASS' : 'SMOKE: FAIL');
  sock.close();
  await finish(ok ? 0 : 1);
}

main().catch(e => { console.error('FAIL:', e.message); finish(1); });
