import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/2.2 旋转位置编码（RoPE）原理与实现/rope-rotation-intuition.png"

fig, axes = plt.subplots(1, 2, figsize=(9, 4.5), dpi=150)

def draw_rotation(ax, theta_deg, title):
    v0 = np.array([1.0, 0.0])
    theta = np.deg2rad(theta_deg)
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    v1 = R @ v0

    ax.annotate("", xy=v0, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#4c72b0", lw=2.5))
    ax.annotate("", xy=v1, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#c44e52", lw=2.5))

    ax.text(v0[0] + 0.05, v0[1] - 0.08, "q (original)", color="#4c72b0", fontsize=10, fontweight="bold")
    ax.text(v1[0] + 0.05, v1[1] + 0.05, f"q' (rotated by pos·θ={theta_deg}°)", color="#c44e52", fontsize=10, fontweight="bold")

    arc_theta = np.linspace(0, theta, 50)
    ax.plot(0.35 * np.cos(arc_theta), 0.35 * np.sin(arc_theta), color="gray", lw=1.2)

    circle = plt.Circle((0, 0), 1.0, fill=False, linestyle="--", color="lightgray")
    ax.add_patch(circle)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])

draw_rotation(axes[0], 30, "Position m=1: rotate by θ")
draw_rotation(axes[1], 90, "Position n=3: rotate by 3θ")

fig.suptitle("RoPE Geometric Intuition: Rotating Q/K by an Angle Proportional to Position", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
