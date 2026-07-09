import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.2 词表大小选择与性能影响/vocab-size-compare.png"

# 数据来源：各模型官方 config.json / 技术报告（详见 1.2.5 正文表格的来源链接）
families = {
    "GPT":       [("GPT-2", 50257), ("GPT-4\n(cl100k)", 100277), ("GPT-4o\n(o200k)", 200019)],
    "Llama":     [("Llama1/2", 32000), ("Llama3+", 128256), ("Llama4", 202048)],
    "Qwen":      [("Qwen2", 151646), ("Qwen2.5/3", 151936), ("Qwen3.5/3.6", 248320)],
    "DeepSeek":  [("DeepSeek-V2", 102400), ("DeepSeek-V3/R1", 129280)],
    "GLM":       [("ChatGLM", 130528), ("ChatGLM2/3", 65024), ("GLM-4+", 151552)],
    "MiniMax":   [("MiniMax-Text-01", 200064), ("MiniMax-M2", 200064)],
}
family_colors = {
    "GPT": "#4c72b0", "Llama": "#55a868", "Qwen": "#c44e52",
    "DeepSeek": "#8172b2", "GLM": "#ccb974", "MiniMax": "#64b5cd",
}

labels, values, colors, group_bounds = [], [], [], []
idx = 0  # 纯整数索引，对应 labels/values/x 的下标
for fam, items in families.items():
    start_idx = idx
    for name, v in items:
        labels.append(name)
        values.append(v)
        colors.append(family_colors[fam])
        idx += 1
    group_bounds.append((fam, start_idx, idx - 1))

x = []
cursor = 0.0
for fam, items in families.items():
    for _ in items:
        x.append(cursor)
        cursor += 1
    cursor += 0.6  # 组间留白

fig, ax = plt.subplots(figsize=(11, 5.2), dpi=150)
bars = ax.bar(x, values, color=colors, width=0.75)

for xi, v in zip(x, values):
    ax.text(xi, v + 3000, f"{v:,}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)

# 组标签（系列名）放在 x 轴下方更远处
for fam, start, end in group_bounds:
    center = (x[start] + x[end]) / 2
    ax.text(center, -max(values) * 0.13, fam, ha="center", va="top",
            fontsize=10.5, fontweight="bold", color=family_colors[fam])

ax.set_ylabel("Vocabulary Size (V)", fontsize=11)
ax.set_title("Vocabulary Size by Model Family (grouped, chronological within family)",
             fontsize=13, fontweight="bold", pad=14)
ax.set_ylim(0, max(values) * 1.18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.subplots_adjust(bottom=0.22)

fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
