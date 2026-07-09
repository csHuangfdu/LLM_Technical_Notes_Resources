import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.3 中英文分词效率差异/zh-en-token-count.png"

# 数据来自正文 1.3.3 表格：真实实测 CPT（characters per token，越大越省 token）
# 来源：Mason AI Lab 2026-04 六项任务实测均值（https://masonailab.com/insights/token-efficiency/）
tokenizers = [
    "GPT-4\ncl100k_base",
    "Llama 3\nseries",
    "GPT-4o\no200k_base",
    "Gemini 3.x",
    "Claude\nOpus 4.6",
    "Qwen\nseries",
    "DeepSeek\nV3/V4",
]
en_cpt = [5.4, 5.3, 5.4, 5.5, 5.5, 4.8, 5.0]
zh_cpt = [0.75, 1.0, 1.15, 1.0, 1.05, 1.2, 1.15]  # 取正文区间中值

x = range(len(tokenizers))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
b1 = ax.bar([i - width / 2 for i in x], en_cpt, width, label="English CPT", color="#4c72b0")
b2 = ax.bar([i + width / 2 for i in x], zh_cpt, width, label="Chinese CPT", color="#c44e52")

for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.08, f"{h:g}",
                ha="center", va="bottom", fontsize=8.5)

ax.axhline(y=1.0, color="gray", linestyle=":", linewidth=1, alpha=0.6)
ax.text(len(tokenizers) - 0.5, 1.05, "CPT=1.0 (1 char ≈ 1 token)", fontsize=7.5, color="gray", ha="right")

ax.set_xticks(list(x))
ax.set_xticklabels(tokenizers, fontsize=8.5)
ax.set_ylabel("Characters per Token (CPT, higher = more efficient)", fontsize=10.5)
ax.set_title("English vs Chinese tokenizer efficiency (real benchmark, 2026-04)", fontsize=12, fontweight="bold", pad=12)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
