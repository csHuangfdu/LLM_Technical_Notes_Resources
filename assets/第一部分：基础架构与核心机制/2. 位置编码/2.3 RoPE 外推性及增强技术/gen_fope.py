"""FoPE 频谱处理示意：RoPE 是每维单频率 e^{i n theta_d}，
FoPE 把每维扩展为傅里叶级数（主频率 + 谐波），并对训练中"转不足一圈"
（omega < 2pi/N）的低频分量置零，避免欠训练频谱损伤。

图中对比三件事：
1. RoPE 单频率基（每条竖线一个维度频率）
2. FoPE 谐波扩展（主频率周围有谐波频点）
3. 低频截断（omega < 2pi/N 的区域被置零，红色阴影）
用于直观说明"低频截断 + 谐波扩展"。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

fm.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术/fope-frequency-zeroing.png"

BASE = 10000.0
DIM = 64
N = 4096  # 训练长度
omega_l = 2 * np.pi / N  # 低频截断阈值

i = np.arange(DIM // 2)
theta = BASE ** (-2.0 * i / DIM)  # RoPE 每维角频率

fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)

# 画 RoPE 原始频点（黑色小刻度）
for t in theta:
    ax.axvline(t, ymin=0.42, ymax=0.78, color="#4c72b0", linewidth=1.0, alpha=0.7)

# 画 FoPE 谐波扩展（主频率周围小偏移，绿色刻度）
rng = np.random.default_rng(7)
for t in theta:
    for _ in range(2):
        h = t * (1 + rng.normal(0, 0.15))
        if h > 0:
            ax.axvline(h, ymin=0.08, ymax=0.35, color="#55a868", linewidth=0.7, alpha=0.5)

# 低频截断区
ax.axvspan(0, omega_l, color="#c44e52", alpha=0.18)
ax.axvline(omega_l, color="#c44e52", linestyle="--", linewidth=1.4)

ax.set_xscale("log")
ax.set_xlim(1e-4, 1.2)
ax.set_xlabel(r"角频率 $\omega_d$（对数刻度）")
ax.set_yticks([])
ax.set_title(r"FoPE：低频截断（$\omega<\omega_l=2\pi/N$ 置零）+ 傅里叶谐波扩展",
             fontsize=11, fontweight="bold")
ax.text(omega_l * 1.4, 0.9, r"截断阈值 $\omega_l=2\pi/N$", color="#c44e52", fontsize=9,
        transform=ax.get_xaxis_transform())
ax.text(1e-3, 0.98, "低频区\n(训练转不足一圈 → 置零)", color="#c44e52", fontsize=9,
        transform=ax.get_xaxis_transform(), ha="center")
ax.text(0.4, 0.98, "主频率(蓝) + 谐波(绿)\n(傅里叶级数)", color="#2f4f4f", fontsize=9,
        transform=ax.get_xaxis_transform(), ha="center")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
