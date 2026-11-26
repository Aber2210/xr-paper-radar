# -*- coding: utf-8 -*-
"""标题级扩展词补扫表（第三层召回，2026-11-14 起固化；不计入 RSS 漏网统计）。

2026-11-27 抽出为独立模块：此前 `missed_xr_*.py` import triage 脚本时会把 triage 顶层
整段重跑（重写 xr_pool / old_replace / nonxr），11-26 批次已踩过一次（结果幂等但风险高）。
今后扩展词只改本文件，triage 与 missed 脚本共同 import。
"""

EXTRA = [
    "virtual reality", "augmented reality", "mixed reality", "spatial", "immersive",
    "head mounted", "goggles", "stereo", "3d reconstruction", "novel view",
    "view synthesis", "point cloud", "mesh", "6-dof", "pose estimation",
    "hand", "gaze", "user study", "presence", "teleoperation", "sim-to-real",
    "gaussian", "radiance field", "depth", "visual odometry", "tracking",
    # 2026-11-19 登记的语义缺口词（tactile/SDF/meshing/单光子/单目深度等）
    "tactile", "taxel", "sdf", "meshing", "affine", "bundle adjustment",
    "light field", "image-based rendering", "single-photon", "spad",
    "monocular depth", "nerf", "splatting", "slam", "voxel", "avatar",
]
