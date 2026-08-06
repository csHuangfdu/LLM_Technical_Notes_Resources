"""重绘 RoPE 在训练长度（16K）之外出现震荡的衰减曲线（原图带水印，本脚本用
RoFormer 长程衰减公式 C(s)=sum_i cos(s*theta_i) 复现相同现象，而非复制原图）。

模拟设定：训练长度 L_train=16384，取 d=128（贴近典型注意力头维度），观察 s 从
0 扫到约 64K 时衰减曲线的行为——理论上超出训练长度越多，累加的高频分量相位越
容易随机对齐/抵消，数值上呈现出震荡而非单调衰减。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术（NTK ／ PI ／ YaRN ／ ReRoPE ／ ALiBi）/rope-decay-16k-oscillation.png"

BASE = 10000.0
DIM = 128
L_TRAIN = 16384


def decay_curve(dim: int, s: np.ndarray, base: float = BASE) -> np.ndarray:
    i = np.arange(dim // 2)
    theta = base ** (-2.0 * i / dim)
    return np.array([np.sum(np.cos(sv * theta)) for sv in s])


s = np.arange(0, 65536, 64)
curve = decay_curve(DIM, s)

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
ax.plot(s, curve, color="#4c72b0", linewidth=1.0, label="RoPE decay C(s)")
ax.axvline(L_TRAIN, color="#c44e52", linestyle="--", linewidth=1.3,
           label=f"Training length L_train={L_TRAIN}")
ax.axvspan(L_TRAIN, s.max(), color="#c44e52", alpha=0.06)
ax.text(L_TRAIN * 1.05, curve.max() * 0.85, "Unseen range\n(direct extrapolation)",
        color="#c44e52", fontsize=9)

ax.set_xlabel("Relative position difference s = m - n")
ax.set_ylabel(r"$C(s)=\sum_i \cos(s\cdot\theta_i)$")
ax.set_title("RoPE Decay Curve: Smooth Within Training Length, Oscillates Beyond It\n(self-computed, dim=128, base=10000)",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
