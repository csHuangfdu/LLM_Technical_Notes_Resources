import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.2 词表大小选择与性能影响/vocab-size-compare.png"

models = ["GPT-2", "LLaMA/LLaMA2", "ChatGLM3", "LLaMA3", "Qwen2"]
vocab_sizes = [50257, 32000, 65024, 128256, 151646]
colors = ["#4c72b0", "#55a868", "#c44e52", "#8172b2", "#ccb974"]

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
bars = ax.bar(models, vocab_sizes, color=colors, width=0.6)

for bar, v in zip(bars, vocab_sizes):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 2000, f"{v:,}",
            ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_ylabel("Vocabulary Size (V)", fontsize=11)
ax.set_title("Vocabulary Size Comparison Across Models", fontsize=13, fontweight="bold", pad=12)
ax.set_ylim(0, max(vocab_sizes) * 1.18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
