import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.2 词表大小选择与性能影响/vocab-size-compare.png"

# 数据来源：各模型官方 config.json / 技术报告（详见 1.2.5 正文表格的来源链接）
# 修复记录：旧版用 "\n" 手动换行 + 不旋转标签，导致 Qwen2/Qwen2.5/3、ChatGLM/ChatGLM2/3、
# MiniMax-Text-01/MiniMax-M2 等相邻标签横向重叠。改为「全部单行 + 旋转 32°」后不再重叠，
# 且不需要为个别标签单独换行（统一处理方式更不易在后续加模型时再次踩坑）。
families = {
    "GPT":       [("GPT-2", 50257), ("GPT-4 (cl100k)", 100277), ("GPT-4o (o200k)", 200019)],
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
    cursor += 0.8  # 组间留白（比旧版 0.6 更宽，配合旋转标签留出呼吸空间）

fig, ax = plt.subplots(figsize=(13.5, 6.4), dpi=150)
bars = ax.bar(x, values, color=colors, width=0.72)

# 数值标签防重叠：相邻两根柱子数值非常接近（差值 < 量级的 3%）时，柱子几乎等高，
# 标签会紧贴在一起甚至看起来连成一片（真实案例：Qwen2 151,646 与 Qwen2.5/3 151,936
# 几乎相等；MiniMax-Text-01 与 MiniMax-M2 的 200,064 完全相同）。这里让"当前值与上一个
# 值足够接近"的标签整体上移一个偏移量，与前一个标签的高度错开，避免视觉粘连。
value_range = max(values) - min(values)
close_threshold = value_range * 0.03
label_offsets = [0] * len(values)
for i in range(1, len(values)):
    if abs(values[i] - values[i - 1]) < close_threshold:
        label_offsets[i] = value_range * 0.045

for xi, v, off in zip(x, values, label_offsets):
    ax.text(xi, v + 3000 + off, f"{v:,}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

ax.set_xticks(x)
# 旋转 32°+右对齐：比水平排列节省横向空间，彻底避开相邻短标签重叠
# （旧版 Qwen2/Qwen2.5/3、ChatGLM/ChatGLM2/3、MiniMax-Text-01/MiniMax-M2 重叠问题的根因）
ax.set_xticklabels(labels, fontsize=9, rotation=32, ha="right", rotation_mode="anchor")

# 组标签（系列名）放在旋转后的模型名标签下方，留足垂直间距避免与其相碰
for fam, start, end in group_bounds:
    center = (x[start] + x[end]) / 2
    ax.text(center, -max(values) * 0.34, fam, ha="center", va="top",
            fontsize=11.5, fontweight="bold", color=family_colors[fam])

ax.set_ylabel("Vocabulary Size (V)", fontsize=11)
ax.set_title("Vocabulary Size by Model Family (grouped, chronological within family)",
             fontsize=13.5, fontweight="bold", pad=14)
ax.set_ylim(0, max(values) * 1.18)
ax.set_xlim(x[0] - 0.8, x[-1] + 0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.subplots_adjust(bottom=0.34)

fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
