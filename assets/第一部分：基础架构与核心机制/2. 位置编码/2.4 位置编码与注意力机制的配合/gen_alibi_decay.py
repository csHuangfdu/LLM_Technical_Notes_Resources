import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.4 位置编码与注意力机制的配合/alibi-linear-decay.png"

distance = np.linspace(0, 100, 200)
slopes = [0.5, 0.25, 0.125, 0.0625]  # 不同 head 的斜率 m（几何递减，与 ALiBi 论文设计思路一致）
colors = ["#c44e52", "#4c72b0", "#55a868", "#8172b2"]

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
for m, c in zip(slopes, colors):
    penalty = -m * distance
    ax.plot(distance, penalty, label=f"head slope m={m}", color=c, lw=2)

ax.set_xlabel("Relative distance |i - j|", fontsize=11)
ax.set_ylabel("Attention score penalty (-m·|i-j|)", fontsize=11)
ax.set_title("ALiBi: Linear Distance Penalty Across Different Heads", fontsize=12, fontweight="bold", pad=10)
ax.legend(fontsize=9)
ax.grid(linestyle="--", alpha=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
