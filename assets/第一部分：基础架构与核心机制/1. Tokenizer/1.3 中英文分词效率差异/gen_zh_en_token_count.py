import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib import font_manager
font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.3 中英文分词效率差异/zh-en-token-count.png"

# 数据严格只取正文 1.3.6 表格三行示例数据（CPT = 字符数 / token 数，越大越省 token）。
# 图为示例性展示，非权威排名；真实计数随 tokenizer 版本与样本变化，以 1.3.6 表为准。
tokenizers = [
    "OpenAI cl100k_base\n（GPT-4）",
    "Qwen2\ntokenizer",
    "DeepSeek-V2\ntokenizer",
]
zh_cpt = [0.56, 1.43, 0.91]
en_cpt = [4.0, 4.0, 4.2]

x = range(len(tokenizers))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
b1 = ax.bar([i - width / 2 for i in x], zh_cpt, width, label="中文 CPT", color="#c44e52")
b2 = ax.bar([i + width / 2 for i in x], en_cpt, width, label="英文 CPT", color="#4c72b0")

for bars in (b1, b2):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.08, f"{h:g}",
                ha="center", va="bottom", fontsize=9)

ax.axhline(y=1.0, color="gray", linestyle=":", linewidth=1, alpha=0.6)
ax.text(len(tokenizers) - 0.5, 1.05, "CPT=1.0（1 字符 ≈ 1 token）", fontsize=7.5, color="gray", ha="right")

ax.set_xticks(list(x))
ax.set_xticklabels(tokenizers, fontsize=9)
ax.set_ylabel("Characters per Token（CPT，越大越省）", fontsize=10.5)
ax.set_title("三种 tokenizer 的中英文 CPT（示例实测，与 1.3.6 表一致）",
             fontsize=12, fontweight="bold", pad=12)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
