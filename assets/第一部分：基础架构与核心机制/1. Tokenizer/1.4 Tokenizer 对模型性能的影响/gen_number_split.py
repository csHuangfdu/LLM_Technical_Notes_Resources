import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.4 Tokenizer 对模型性能的影响/number-split-inconsistency.png"

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
ax.axis("off")

def draw_split(y, number, splits, colors, label):
    ax.text(-0.3, y, label, fontsize=10, va="center", ha="right", fontweight="bold")
    x = 0
    for seg, c in zip(splits, colors):
        w = len(seg) * 0.45
        rect = mpatches.FancyBboxPatch((x, y - 0.28), w, 0.56,
                                        boxstyle="round,pad=0.02", linewidth=1.2,
                                        edgecolor="black", facecolor=c)
        ax.add_patch(rect)
        ax.text(x + w / 2, y, seg, ha="center", va="center", fontsize=13, fontweight="bold")
        x += w + 0.08

draw_split(3.2, "1234", ["123", "4"], ["#8ecae6", "#ffb703"], 'Context A: "the year 1234 AD"')
draw_split(2.0, "1234", ["1", "234"], ["#8ecae6", "#ffb703"], 'Context B: "item No.1234"')
draw_split(0.8, "1234", ["1234"], ["#95d5b2"], 'Context C: "id=1234"')

ax.set_xlim(-3.6, 4)
ax.set_ylim(0, 4)
ax.set_title(
    'Same number "1234", different tokenizer splits by context\n'
    '(split depends on training-corpus frequency, not numeric meaning)',
    fontsize=11, fontweight="bold", pad=10,
)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
