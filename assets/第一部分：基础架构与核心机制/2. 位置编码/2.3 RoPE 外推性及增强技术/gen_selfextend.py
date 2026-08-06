"""SelfExtend 双层注意力示意：近处 neighbor attention 保留原始相对位置，
远处 grouped attention 按组压缩（floor 除法）后封顶，两组 attention 合并。

图中画出"实际代入 RoPE 的组索引 g(j)"随 key 位置 j 的变化：
- j <= w 的区域：g(j) = j（neighbor，逐 token 精度）
- j > w 的区域：g(j) = w + floor((j-w)/k)，阶梯状压缩（grouped）
用于直观对比 ReRoPE（窗口外恒为常数）与 PI（全局线性压缩）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

fm.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术/selfextend-grouped-attention.png"

W = 24      # neighbor window w（示意值）
K = 6       # group size（示意值）
L = 90      # 展示到 90

j = np.arange(0, L + 1)
g = np.where(j <= W, j, W + np.floor((j - W) / K).astype(int))

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
ax.plot(j[: W + 1], g[: W + 1], color="#4c72b0", linewidth=2,
        label="neighbor attention：$g(j)=j$（窗口内逐 token 精度）")
ax.plot(j[W:], g[W:], color="#c44e52", linewidth=2, marker="o", markersize=3,
        label="grouped attention：$g(j)=w+\\lfloor (j-w)/k\\rfloor$（窗口外按组压缩）")
ax.axvline(W, color="#8172b2", linestyle="--", linewidth=1.3, label=f"窗口边界 $w={W}$")
ax.set_xlabel("key 位置 $j$")
ax.set_ylabel("实际代入 RoPE 的位置 $g(j)$")
ax.set_title("SelfExtend：近处逐 token、远处按组压缩的双层位置映射（示意值 $w=24, k=6$）",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
