"""YaRN attention scaling 概念曲线：scaling = 0.1*ln(s) + 1，s=L_test/L_train
随扩展倍率 s 增长，scaling 递减（<=1），使 softmax 更尖锐。

图中对比三条曲线：1.0（无缩放基线）、YaRN 公式的 0.1*ln(s)+1、
以及文献中常见的 0.07*ln(s)+1 变体，便于直观理解"扩展越长、scaling 越小"。
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

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.3 RoPE 外推性及增强技术/yarn-attention-scaling.png"

s = np.linspace(1, 32, 200)
yarn_a = 0.1 * np.log(s) + 1
yarn_b = 0.07 * np.log(s) + 1

fig, ax = plt.subplots(figsize=(7, 3.8), dpi=150)
ax.plot(s, np.ones_like(s), color="#888", linestyle=":", linewidth=1.3,
        label=r"baseline $\sqrt{1/t}=1$ (no scaling)")
ax.plot(s, yarn_a, color="#4c72b0", linewidth=2.0,
        label=r"YaRN: $\sqrt{1/t}=0.1\ln s + 1$")
ax.plot(s, yarn_b, color="#c44e52", linewidth=2.0, linestyle="--",
        label=r"variant: $\sqrt{1/t}=0.07\ln s + 1$")
ax.axhline(0, color="#444", linewidth=0.6)
ax.set_xlabel(r"扩展倍率 $s = L_{test} / L_{train}$")
ax.set_ylabel(r"attention scaling $\sqrt{1/t}$")
ax.set_title("YaRN attention scaling：s 越大（扩得越长），scaling 越小，softmax 越尖", fontsize=11)
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
