# -*- coding: utf-8 -*-
"""导出 2026-10-02 批次全部新论文的「完整摘要 + 自动赛道猜测」供人工 7 维打分。"""
import json

NEW = "data/raw/2026-10-02_new.jsonl"
OUT = "data/raw/1002_full_abstracts.txt"

TRACK_KW = {
    "渲染与显示": ["near-eye","light field","waveguide","holographic","varifocal","maxwellian","retinal projection","pancake","foveated","accommodation","display","头显","near eye"],
    "重建与SLAM": ["slam","3d reconstruction","reconstruction","mapping","localization","odometry","vio","rgb-d","point cloud","depth estimation","lidar","structure from motion","sfm"],
    "神经渲染": ["3d gaussian","gaussian splatting","3dgs","nerf","neural radiance","splatting","novel view","neural rendering","radiance field"],
    "交互与输入": ["interaction","input","controller","gesture","menu","ui ","user interface","navigation","teleport","select"],
    "触觉与多模态": ["haptic","tactile","thermal","olfact","smell","audio","sound","multimodal","multimodal"],
    "化身与人体": ["avatar","human","body","hand","face","head","motion capture","animation","talking","digital human","virtual human","character"],
    "空间计算与UI": ["spatial computing","augmented reality","mixed reality","extended reality","ar ","mr ","xr ","spatial","scene understanding","caption"],
    "感知与认知": ["egocentric","egocenter","perception","cognition","attention","gaze","eye tracking","understanding","benchmark","dataset","reasoning"],
    "系统与平台": ["system","platform","framework","runtime","compiler","streaming","compression","codec","edge","distributed","latency","real-time","real time"],
    "内容生成": ["generation","generative","diffusion","text-to","image-to","synthesize","scene generation","content"],
    "世界模型与仿真": ["world model","world action","simulation","simulator","sim2real","digital twin","digital twin"],
    "评估与数据集": ["benchmark","dataset","evaluation","survey","study","dataset","assessment","taxonomy"],
}

def guess_track(r):
    blob = (r["title"] + " " + r["abstract"]).lower()
    # 优先级：更具体的先
    order = ["渲染与显示","触觉与多模态","化身与人体","重建与SLAM","神经渲染","空间计算与UI",
             "交互与输入","感知与认知","世界模型与仿真","内容生成","系统与平台","评估与数据集"]
    best, best_n = "神经渲染", 0
    for t in order:
        n = sum(1 for k in TRACK_KW[t] if k in blob)
        if n > best_n:
            best, best_n = t, n
    return best

recs = [json.loads(l) for l in open(NEW, encoding="utf-8") if l.strip()]
recs.sort(key=lambda r: r["published"][:10], reverse=True)
with open(OUT, "w", encoding="utf-8") as f:
    for r in recs:
        f.write(f"\n### {r['base_id']} | {r['published'][:10]} | guess:{guess_track(r)}\n")
        f.write(f"TITLE: {r['title']}\n")
        f.write(f"ABSTRACT: {r['abstract']}\n")
print("dumped", len(recs), "->", OUT)
