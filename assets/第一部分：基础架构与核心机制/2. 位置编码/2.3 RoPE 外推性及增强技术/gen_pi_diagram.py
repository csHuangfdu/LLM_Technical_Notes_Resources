"""重绘 Position Interpolation (PI) 核心直觉示意图（原图带水印，本脚本用真实
sin 曲线 + numpy 采样点重新绘制同样的对比逻辑：正常做法在训练区间外出现"未见相位"，
PI 把更长序列的位置整体压缩回训练区间内）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术（NTK ／ PI ／ YaRN ／ ReRoPE ／ ALiBi）/position-interpolation-diagram.png"

L_TRAIN = 2048
L_NEW = 4096
FREQ = 2 * np.pi / 1024  # 选一个便于可视化的周期

fig, axes = plt.subplots(2, 1, figsize=(8, 6), dpi=150, sharex=True)

# --- 上图：正常做法（直接外推），训练区间内为蓝点，训练区间外为红点（未见相位） ---
ax = axes[0]
x_full = np.arange(0, L_NEW, 40)
y_full = np.sin(FREQ * x_full)
x_smooth = np.linspace(0, L_NEW, 800)
ax.plot(x_smooth, np.sin(FREQ * x_smooth), color="#4c72b0", linewidth=1.2, alpha=0.6)
in_range = x_full <= L_TRAIN
ax.scatter(x_full[in_range], y_full[in_range], color="#4c72b0", s=25, zorder=3, label="Pre-trained range")
ax.scatter(x_full[~in_range], y_full[~in_range], color="#c44e52", s=25, zorder=3, label="Unseen range (extrapolation)")
ax.axvspan(L_TRAIN, L_NEW, color="#c44e52", alpha=0.06)
ax.axvline(L_TRAIN, color="gray", linestyle="--", linewidth=1)
ax.set_title("Normal (direct extrapolation): unseen phase beyond training range", fontsize=10.5)
ax.set_ylabel("RoPE value")
ax.set_xticks([0, L_TRAIN, L_NEW])
ax.legend(fontsize=8.5, loc="lower right")

# --- 下图：Position Interpolation，把 [0, L_new) 压缩映射回 [0, L_train) ---
ax = axes[1]
x_new = np.arange(0, L_NEW, 40)
x_compressed = x_new * (L_TRAIN / L_NEW)          # PI 的位置映射: pos' = pos * L_train/L_new
y_compressed = np.sin(FREQ * x_compressed)
x_smooth2 = np.linspace(0, L_TRAIN, 800)
ax.plot(x_smooth2, np.sin(FREQ * x_smooth2), color="#4c72b0", linewidth=1.2, alpha=0.6)
in_range2 = x_new <= L_TRAIN
ax.scatter(x_compressed[in_range2], y_compressed[in_range2], color="#4c72b0", s=25, zorder=3, label="Original positions")
ax.scatter(x_compressed[~in_range2], y_compressed[~in_range2], color="#55a868", s=25, zorder=3,
           label="Compressed positions (originally beyond L_train)")
ax.set_title(r"Position Interpolation: $pos' = pos \cdot L_{train}/L_{new}$, all mapped back into pre-trained range",
             fontsize=10.5)
ax.set_ylabel("RoPE value")
ax.set_xlabel("Position")
ax.set_xticks([0, L_TRAIN])
ax.legend(fontsize=8.5, loc="lower right")

for a in axes:
    a.grid(alpha=0.3)
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)

fig.suptitle("Position Interpolation (PI): Compress Unseen Range Back into Pre-trained Range",
             fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
