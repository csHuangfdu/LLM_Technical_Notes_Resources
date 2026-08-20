"""R1 蒸馏 vs 小模型自训 RL 对比柱状图（论文 Table 6 核心结论）：
QwQ-32B-Preview / R1-Zero-Qwen-32B(自训RL) / R1-Distill-Qwen-32B(蒸馏) 在
AIME2024、MATH-500、GPQA Diamond、LiveCodeBench 四基准上的 pass@1。
直观展示"蒸馏全面碾压小模型自训 RL"。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

fm.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/6. 模型架构演进与代表模型/6.2 文本大模型/6.2.4 DeepSeek 系列/r1-distill-vs-rl-32b.png"

labels = ["AIME 2024", "MATH-500", "GPQA Diamond", "LiveCodeBench"]
qpq = [50.0, 90.6, 54.5, 41.9]
rl = [47.0, 91.6, 55.0, 40.2]
distill = [72.6, 94.3, 62.1, 57.2]

x = np.arange(len(labels))
width = 0.26

fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=150)
b1 = ax.bar(x - width, qpq, width, label="QwQ-32B-Preview", color="#4c72b0")
b2 = ax.bar(x, rl, width, label="R1-Zero-Qwen-32B（小模型自训 RL）", color="#dd8452")
b3 = ax.bar(x + width, distill, width, label="R1-Distill-Qwen-32B（蒸馏）", color="#55a868")

for bars in (b1, b2, b3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.2, f"{h:.1f}",
                ha="center", va="bottom", fontsize=8)

ax.set_ylabel("pass@1（%）")
ax.set_title("DeepSeek-R1 蒸馏 vs 小模型自训 RL（Qwen-32B 对照，论文 Table 6）", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(fontsize=8.5)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, 102)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
