"""重绘 RoPE 原始版 vs 做了 Position Interpolation (PI) 后的衰减对比（原图带水印，
本脚本用 RoFormer 衰减公式计算，PI 版本等价于把位置 pos 替换为 pos * L_train/L_new
再代入同样的衰减公式）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术（NTK ／ PI ／ YaRN ／ ReRoPE ／ ALiBi）/rope-decay-64k-pi-vs-base.png"

BASE = 10000.0
DIM = 128
L_TRAIN = 16384
L_NEW = 65536


def decay_curve(dim: int, s: np.ndarray, base: float = BASE) -> np.ndarray:
    i = np.arange(dim // 2)
    theta = base ** (-2.0 * i / dim)
    return np.array([np.sum(np.cos(sv * theta)) for sv in s])


s = np.arange(0, L_NEW, 64)
curve_base = decay_curve(DIM, s)                                  # 原始 RoPE，直接外推
curve_pi = decay_curve(DIM, s * (L_TRAIN / L_NEW))                 # PI：位置先压缩再代入

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
ax.plot(s, curve_base, color="#dd8452", linewidth=1.0, label="RoPE (direct extrapolation)")
ax.plot(s, curve_pi, color="#4c72b0", linewidth=1.0, label="RoPE + PI (position interpolation)")
ax.axvline(L_TRAIN, color="gray", linestyle=":", linewidth=1, alpha=0.7)
ax.text(L_TRAIN * 1.02, curve_base.max() * 0.9, "L_train", color="gray", fontsize=8.5)

ax.set_xlabel("Relative position difference s = m - n")
ax.set_ylabel(r"$C(s)=\sum_i \cos(s\cdot\theta_i)$")
ax.set_title("RoPE Decay at 64K: Original vs. Position-Interpolated\n(self-computed, dim=128, L_train=16384 → L_new=65536)",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
