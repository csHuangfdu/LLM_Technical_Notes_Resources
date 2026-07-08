import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.3 中英文分词效率差异/zh-en-token-count.png"

# 数据来自正文 1.3.3 表格：约20字中文句子 vs 对应英文同义句(约15词) 的 token 数量级(取区间中值)，示意性对比
tokenizers = ["GPT-2 BPE\n(original)", "LLaMA/LLaMA2\nSentencePiece", "GPT-4\ncl100k_base", "Qwen2/ChatGLM3\n(zh-optimized)"]
zh_tokens = [37.5, 30, 24, 16]
en_tokens = [15, 15, 15, 15]

x = range(len(tokenizers))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
b1 = ax.bar([i - width / 2 for i in x], zh_tokens, width, label="Chinese sentence (~20 chars)", color="#c44e52")
b2 = ax.bar([i + width / 2 for i in x], en_tokens, width, label="English equivalent (~15 words)", color="#4c72b0")

for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:g}",
                ha="center", va="bottom", fontsize=9)

ax.set_xticks(list(x))
ax.set_xticklabels(tokenizers, fontsize=9)
ax.set_ylabel("Token count (illustrative midpoint)", fontsize=11)
ax.set_title("Same content: Chinese vs English token count by tokenizer (illustrative)", fontsize=11, fontweight="bold", pad=12)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
