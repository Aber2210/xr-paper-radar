# -*- coding: utf-8 -*-
import json
NEW = "data/raw/2026-10-02_new.jsonl"
OUT = "data/raw/1002_compact.txt"
TRACK_KW = {
 "渲染与显示": ["near-eye","light field","waveguide","holographic","varifocal","maxwellian","retinal projection","pancake","foveated","accommodation","display"],
 "重建与SLAM": ["slam","3d reconstruction","reconstruction","mapping","localization","odometry","vio","rgb-d","point cloud","depth estimation","lidar","structure from motion"],
 "神经渲染": ["3d gaussian","gaussian splatting","3dgs","nerf","neural radiance","splatting","novel view","neural rendering","radiance field"],
 "交互与输入": ["interaction","input","controller","gesture","menu","user interface","navigation","teleport"],
 "触觉与多模态": ["haptic","tactile","thermal","olfact","smell","audio-","multimodal"],
 "化身与人体": ["avatar","human","body","hand","face","head","motion capture","animation","talking","digital human","virtual human","character"],
 "空间计算与UI": ["spatial computing","augmented reality","mixed reality","extended reality","ar ","mr ","xr ","spatial","scene understanding","caption"],
 "感知与认知": ["egocentric","egocenter","perception","cognition","attention","gaze","eye tracking","understanding","benchmark","dataset","reasoning"],
 "系统与平台": ["system","platform","framework","runtime","compiler","streaming","compression","codec","edge","distributed","latency","real-time","real time"],
 "内容生成": ["generation","generative","diffusion","text-to","image-to","synthesize","scene generation","content"],
 "世界模型与仿真": ["world model","world action","simulation","simulator","sim2real","digital twin"],
 "评估与数据集": ["benchmark","dataset","evaluation","survey","study","assessment","taxonomy"],
}
def guess_track(r):
    blob=(r["title"]+" "+r["abstract"]).lower()
    order=["渲染与显示","触觉与多模态","化身与人体","重建与SLAM","神经渲染","空间计算与UI","交互与输入","感知与认知","世界模型与仿真","内容生成","系统与平台","评估与数据集"]
    best,bn="神经渲染",0
    for t in order:
        n=sum(1 for k in TRACK_KW[t] if k in blob)
        if n>bn: best,bn=t,n
    return best
recs=[json.loads(l) for l in open(NEW,encoding="utf-8") if l.strip()]
recs.sort(key=lambda r:r["published"][:10], reverse=True)
with open(OUT,"w",encoding="utf-8") as f:
    for r in recs:
        a=r["abstract"]
        if len(a)>380: a=a[:380]+"…"
        f.write(f"[{r['base_id']}] {r['published'][:10]} | {guess_track(r)}\n  {r['title']}\n  {a}\n")
print("compact dumped", len(recs))
