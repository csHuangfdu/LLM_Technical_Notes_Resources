import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.1 绝对位置编码 vs 相对位置编码/sinusoidal-pe-heatmap.png"

d_model = 128
max_pos = 100
pos = np.arange(max_pos)[:, None]
dim = np.arange(d_model)[None, :]

angle_rates = 1.0 / np.power(10000, (2 * (dim // 2)) / np.float32(d_model))
angle_rads = pos * angle_rates
pe = np.zeros((max_pos, d_model))
pe[:, 0::2] = np.sin(angle_rads[:, 0::2])
pe[:, 1::2] = np.cos(angle_rads[:, 1::2])

fig, axes = plt.subplots(1, 2, figsize=(9, 4.5), dpi=150, gridspec_kw={"width_ratios": [1.3, 1]})

im = axes[0].imshow(pe.T, aspect="auto", cmap="RdBu", origin="lower")
axes[0].set_xlabel("Position (pos)", fontsize=10)
axes[0].set_ylabel("Embedding dimension (i)", fontsize=10)
axes[0].set_title("Sinusoidal Positional Encoding Heatmap", fontsize=11, fontweight="bold")
fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

for i in [2, 20, 60, 120]:
    axes[1].plot(pos[:, 0], pe[:, i], label=f"dim {i}")
axes[1].set_xlabel("Position (pos)", fontsize=10)
axes[1].set_ylabel("PE value", fontsize=10)
axes[1].set_title("PE Curves at Different Dimensions", fontsize=11, fontweight="bold")
axes[1].legend(fontsize=8)
axes[1].grid(linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
