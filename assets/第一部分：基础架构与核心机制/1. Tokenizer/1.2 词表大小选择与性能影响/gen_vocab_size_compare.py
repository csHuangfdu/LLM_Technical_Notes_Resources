import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib import font_manager
font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.2 词表大小选择与性能影响/vocab-size-compare.png"

# 数据严格只取正文 1.2.5 核验表同一字段（config.json 的 vocab_size / 论文报告），
# 非跨字段混图、非排名。来源链接见正文 1.2.5 表格。
models = [
    ("GPT-2", 50257),
    ("Llama 2", 32000),
    ("Llama 3", 128256),
    ("Qwen2.5-7B", 152064),
    ("DeepSeek-V3", 129280),
    ("Gemma 2 9B", 256000),
]

labels = [m[0] for m in models]
values = [m[1] for m in models]

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
bars = ax.bar(range(len(models)), values, color="#4c72b0", width=0.62)

for xi, v in zip(range(len(models)), values):
    ax.text(xi, v + 4000, f"{v:,}", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_xticks(range(len(models)))
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("vocab_size（config 字段）", fontsize=11)
ax.set_title("公开模型词表大小（仅含已核验 vocab_size、非排名）",
             fontsize=13, fontweight="bold", pad=14)
ax.set_ylim(0, max(values) * 1.18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()

fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
