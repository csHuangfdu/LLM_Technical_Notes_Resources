"""DeepSeek-V1 Scaling Law 图表：
(a) IsoFLOP 曲线：不同计算预算下最优模型/数据分配
(b) 超参数 Scaling：最优 Batch Size 和 Learning Rate 随计算预算变化

数据来自论文 arXiv:2401.02954 的公式。
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

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/6. 模型架构演进与代表模型/6.5 DeepSeek 系列/deepseek_v1_scaling_law.png"

# === (a) IsoFLOP 曲线 ===
C = np.logspace(17, 22, 200)  # FLOPs 从 1e17 到 1e22
M_opt = 0.1715 * C**0.5243   # 最优模型规模 (non-embed FLOPs/token)
D_opt = 5.8316 * C**0.4757   # 最优数据规模 (tokens)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=150)

# (a) 模型规模 vs 计算预算
ax1.loglog(C, M_opt, color="#4c72b0", linewidth=2.0)
ax1.set_xlabel("compute budget C (FLOPs)", fontsize=10)
ax1.set_ylabel(r"optimal model size $M_{opt}$ (non-embed FLOPs/token)", fontsize=10)
ax1.set_title("IsoFLOP: optimal model size vs compute budget", fontsize=10, fontweight="bold")
ax1.grid(alpha=0.3)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# 标注 7B 和 67B 的位置
# 7B: ~0.4e9 FLOPs/token → C ≈ 4.5e20
# 67B: ~4e9 FLOPs/token → C ≈ 4.6e22
ax1.annotate(r"7B model", xy=(4.5e20, 0.4e9), xytext=(1e19, 0.8e9),
             arrowprops=dict(arrowstyle="->", color="#c44e52"), fontsize=9, color="#c44e52")
ax1.annotate(r"67B model", xy=(4.6e22, 4e9), xytext=(3e21, 8e9),
             arrowprops=dict(arrowstyle="->", color="#c44e52"), fontsize=9, color="#c44e52")

# (b) 超参数 Scaling
Cb = np.logspace(17, 22, 200)
B_opt = 0.2920 * Cb**0.3271
eta_opt = 0.3118 * Cb**(-0.1250)

ax1b = ax2
ax1b.loglog(Cb, B_opt, color="#4c72b0", linewidth=2.0, label=r"$B_{opt}=0.292\cdot C^{0.327}$")
ax1b.set_xlabel("compute budget C (FLOPs)", fontsize=10)
ax1b.set_ylabel("optimal batch size B (tokens)", fontsize=10, color="#4c72b0")
ax1b.tick_params(axis="y", labelcolor="#4c72b0")
ax1b.grid(alpha=0.3, axis="x")

ax2b = ax1b.twinx()
ax2b.loglog(Cb, eta_opt, color="#c44e52", linewidth=2.0, linestyle="--", label=r"$\eta_{opt}=0.312\cdot C^{-0.125}$")
ax2b.set_ylabel("optimal learning rate $\eta$", fontsize=10, color="#c44e52")
ax2b.tick_params(axis="y", labelcolor="#c44e52")

lines1, labels1 = ax1b.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")
ax2.set_title("Hyperparameter Scaling: B and η vs compute budget", fontsize=10, fontweight="bold")
ax2.spines["top"].set_visible(False)

fig.suptitle("DeepSeek LLM (V1) Scaling Laws (paper: arXiv 2401.02954)", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
