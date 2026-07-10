"""重绘 RoPE 长程衰减性随嵌入维度变化的曲线（原图带水印，本脚本用 RoPE 论文
[RoFormer](https://arxiv.org/abs/2104.09864) 的长程衰减公式重新计算，而非复制原图）。

RoPE 的长程衰减性质：两个方向相同、模长为 1 的向量 q, k 在相对距离 s=m-n 处的
点积期望值为：
    C(s) = sum_{i=0}^{d/2-1} cos(s * theta_i),   theta_i = base^(-2i/d)
这个和随 s 增大而振荡衰减，且维度 d 越大（可用的频率分量越多），衰减曲线越平滑、
振荡出现得越晚 —— 这正是原图想表达的现象，这里用真实公式复现。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.2 旋转位置编码（RoPE）原理与实现/rope-decay-vs-dimension.png"

BASE = 10000.0


def decay_curve(dim: int, max_dist: int) -> np.ndarray:
    i = np.arange(dim // 2)
    theta = BASE ** (-2.0 * i / dim)
    s = np.arange(0, max_dist)
    # C(s) = sum_i cos(s * theta_i)
    return np.array([np.sum(np.cos(sv * theta)) for sv in s])


max_dist = 1024
dims = [512, 1024, 2048, 4096]
colors = ["#4c72b0", "#dd8452", "#55a868", "#c44e52"]

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
for dim, color in zip(dims, colors):
    curve = decay_curve(dim, max_dist)
    ax.plot(curve, label=f"dim={dim}", color=color, linewidth=1.2)

ax.set_xlabel("Relative position difference s = m - n")
ax.set_ylabel(r"$C(s)=\sum_i \cos(s\cdot\theta_i)$  (long-term decay)")
ax.set_title("RoPE Long-term Decay vs. Embedding Dimension\n(self-computed from RoFormer decay formula, base=10000)",
             fontsize=11, fontweight="bold")
ax.legend()
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
