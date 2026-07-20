"""重绘 RoPE / ReRoPE / Leaky ReRoPE 位置矩阵三方对比图（原始笔记 image 65/3/24/69 四张图
各画了一部分，本脚本把三种矩阵重新计算并拼成一张三联图，做到 caption 描述的"左图标准 RoPE、
中图 ReRoPE、右图 Leaky ReRoPE"真正一一对应；矩阵取的是"代入 RoPE 公式的相对位置 pos(i,j)"，
而不是真实距离 i-j 本身）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

fm.fontManager.addfont("/root/.fonts/NotoSansCJKsc-Regular.otf")
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术（NTK ／ PI ／ YaRN ／ ReRoPE ／ ALiBi）/rerope-leaky-window-matrix.png"

N = 12          # 矩阵大小（token 数），够小方便看清数字
W = 5           # 窗口大小 w
K = 2.0         # Leaky ReRoPE 的斜率参数 k（即公式里的 t）


def build_matrix(mode: str) -> np.ndarray:
    """mode: 'rope'（标准 RoPE，pos(i,j)=i-j 无上限）
             'rerope'（ReRoPE，超出 w 后封顶为 w）
             'leaky'（Leaky ReRoPE，超出 w 后按 1/k 缓慢增长）"""
    mat = np.full((N, N), np.nan)
    for i in range(N):
        for j in range(i + 1):  # 下三角（causal，i>=j）
            d = i - j
            if mode == "rope":
                mat[i, j] = d
            elif mode == "rerope":
                mat[i, j] = min(d, W)
            elif mode == "leaky":
                mat[i, j] = min(d, W + (d - W) / K) if d > W else d
    return mat


fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), dpi=150)
titles = [
    "标准 RoPE：pos(i,j) = i-j\n（无上限，随距离无限增长）",
    f"ReRoPE：pos(i,j) = min(i-j, w)\n（窗口 w={W} 外全部封顶）",
    f"Leaky ReRoPE：pos(i,j) = min(i-j, w+(i-j-w)/k)\n（窗口外按 1/k 缓慢增长，k={K}）",
]
modes = ["rope", "rerope", "leaky"]

vmax = N - 1  # 三张图共用同一套颜色刻度，才能横向比较"哪张图数值涨得更快"
for ax, mode, title in zip(axes, modes, titles):
    mat = build_matrix(mode)
    im = ax.imshow(mat, cmap="YlOrRd", vmin=0, vmax=vmax)
    for i in range(N):
        for j in range(i + 1):
            val = mat[i, j]
            txt = f"{val:.1f}" if mode == "leaky" and val != int(val) else f"{int(val)}"
            color = "white" if val > vmax * 0.6 else "black"
            ax.text(j, i, txt, ha="center", va="center", fontsize=6.3, color=color)
    if mode != "rope":
        ax.axhline(W - 0.5 + 0.001, color="#2ca02c", linewidth=0, alpha=0)  # 占位，保持布局一致
    ax.set_title(title, fontsize=9.3)
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels(range(N), fontsize=6.5)
    ax.set_yticklabels(range(N), fontsize=6.5)
    ax.set_xlabel("Key 位置 j", fontsize=8)
    if mode == "rope":
        ax.set_ylabel("Query 位置 i", fontsize=8)

fig.suptitle("代入 RoPE 公式的相对位置矩阵 pos(i,j) 对比（下三角，causal mask）", fontsize=11.5, fontweight="bold")
fig.colorbar(im, ax=axes, orientation="vertical", fraction=0.025, pad=0.02, label="pos(i,j) 数值")
fig.tight_layout(rect=[0, 0, 0.96, 0.94])
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
