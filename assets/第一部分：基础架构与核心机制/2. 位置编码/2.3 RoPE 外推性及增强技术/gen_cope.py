"""CoPE 门控计数示意：位置增量 = 逐 token 的 sigmoid 门控之和，
模型可以选择"哪些 token 算一步"（如只数句子边界、只数非空 token）。

图中用两个假想的 head 展示同一句子的两种计数方式：
- Head A：全部门控=1，p = 原始 token 相对距离（回到 token 计数）
- Head B：只对非空/关键词门控=1，p 只累计"重要 token"，从而不受空白 token 干扰
用于直观说明"counting what's important"。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

fm.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术/cope-gated-counting.png"

# 假设 16 个 token，其中 4 个为"空白/无关 token"（索引 3,6,9,12），其余为重要 token
tokens = np.arange(16)
important = np.ones(16, dtype=bool)
for idx in (3, 6, 9, 12):
    important[idx] = False

# Head A：全部门控=1 → p = 距离
pA = tokens + 1
# Head B：只数重要 token
pB = np.cumsum(important)

fig, axes = plt.subplots(1, 2, figsize=(9.5, 4), dpi=150)

axes[0].bar(tokens, pA, color="#4c72b0", alpha=0.85)
axes[0].set_xlabel("token 下标 $j$")
axes[0].set_ylabel("$p_{ij}$")
axes[0].set_title("Head A：$g_{ij}=1$ 全部计数\n（退化为 token 距离）", fontsize=10)
axes[0].grid(alpha=0.3)

axes[1].bar(tokens, pB, color="#c44e52", alpha=0.85)
for idx in (3, 6, 9, 12):
    axes[1].get_children()
axes[1].set_xlabel("token 下标 $j$")
axes[1].set_ylabel("$p_{ij}$")
axes[1].set_title("Head B：只数重要 token\n$p_{ij}=\\sum g_{ik}$（跳过空白）", fontsize=10)
axes[1].grid(alpha=0.3)
for idx in (3, 6, 9, 12):
    axes[1].axvspan(idx - 0.4, idx + 0.4, color="#8172b2", alpha=0.25)

fig.suptitle("CoPE：位置由门控计数决定，模型自行决定\"什么算一步\"", fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
