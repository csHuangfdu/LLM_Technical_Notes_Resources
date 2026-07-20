"""重绘原始笔记 image 65 / image 69 / image 3 / image 24 四张"抽象符号矩阵"截图
（用 w / L / t 等抽象变量，而非具体数值），拼成一张 2x2 矢量图，与已有的
`rerope-leaky-window-matrix.png`（具体数值热力图版）互补：热力图版直观展示数值
随位置变化的"颜色深浅"趋势，本图还原原始笔记里"逐元素符号化摊开"的呈现方式，
更适合配合正文"矩阵 A / Ã / 合并矩阵"的公式化描述阅读。

四个子图对应关系（原始笔记 图片和附件/ 目录下）：
    image 65.png -> 矩阵 A（步骤①：全局按真实间隔 1 算出，抽象变量 L）
    image 69.png -> 矩阵 Ã（步骤②：全局按 1/t 缩放算出，抽象变量 L、t）
    image  3.png -> ReRoPE 合并矩阵（步骤③：窗口外红→绿，绿色恒为 w，即完全封顶）
    image 24.png -> Leaky ReRoPE 合并矩阵（步骤③：窗口外红→绿，绿色按 w+k/t 递增）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm.fontManager.addfont("/root/.fonts/NotoSansCJKsc-Regular.otf")
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
plt.rcParams["mathtext.fontset"] = "cm"

OUT = (
    "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/2. 位置编码/"
    "2.3 RoPE 外推性及增强技术（NTK ／ PI ／ YaRN ／ ReRoPE ／ ALiBi）/"
    "rerope-abstract-four-matrices.png"
)

BLUE = "#1a56db"
RED = "#d63031"
GREEN = "#1e8449"
DOTS = r"$\ddots$"  # 用 mathtext 渲染省略号，避免 "⋱" 字符缺字体

# 每个矩阵：一个"行列表"，每行是 [(text, color), ...]（右对齐，对应下三角矩阵
# 逐行增多的真实结构；中间省略的行用一整行 DOTS 占位，呼应原图的省略号排布）。
MAT_A = [  # image 65：矩阵 A
    [("0", BLUE)],
    [("1", BLUE), ("0", BLUE)],
    [("2", BLUE), ("1", BLUE), ("0", BLUE)],
    [("3", BLUE), ("2", BLUE), ("1", BLUE), ("0", BLUE)],
    [(DOTS, BLUE), ("3", BLUE), ("2", BLUE), ("1", BLUE), ("0", BLUE)],
    [(DOTS, BLUE), (DOTS, BLUE), ("3", BLUE), ("2", BLUE), ("1", BLUE), ("0", BLUE)],
    [(DOTS, BLUE)] * 5,
    [("L-2", BLUE)] + [(DOTS, BLUE)] * 6,
    [("L-1", BLUE), ("L-2", BLUE)] + [(DOTS, BLUE)] * 3 + [("3", BLUE), ("2", BLUE), ("1", BLUE), ("0", BLUE)],
]

MAT_A_TILDE = [  # image 69：矩阵 Ã = A / t（图中变量名为 k，与正文里的 t 同义）
    [("0", BLUE)],
    [("1/t", BLUE), ("0", BLUE)],
    [("2/t", BLUE), ("1/t", BLUE), ("0", BLUE)],
    [("3/t", BLUE), ("2/t", BLUE), ("1/t", BLUE), ("0", BLUE)],
    [(DOTS, BLUE), ("3/t", BLUE), ("2/t", BLUE), ("1/t", BLUE), ("0", BLUE)],
    [(DOTS, BLUE), (DOTS, BLUE), ("3/t", BLUE), ("2/t", BLUE), ("1/t", BLUE), ("0", BLUE)],
    [(DOTS, BLUE)] * 5,
    [("(L-2)/t", BLUE)] + [(DOTS, BLUE)] * 6,
    [("(L-1)/t", BLUE), ("(L-2)/t", BLUE)] + [(DOTS, BLUE)] * 3 + [("3/t", BLUE), ("2/t", BLUE), ("1/t", BLUE), ("0", BLUE)],
]

MAT_REROPE = [  # image 3：ReRoPE 合并矩阵（红=窗口内取自 A，绿=窗口外恒为 w，完全封顶）
    [("0", RED)],
    [("1", RED), ("0", RED)],
    [("2", RED), ("1", RED), ("0", RED)],
    [(DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w", GREEN), ("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w", GREEN), ("w", GREEN), (DOTS, RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [(DOTS, GREEN), ("w", GREEN), (DOTS, GREEN), (DOTS, RED), (DOTS, RED), (DOTS, RED), (DOTS, RED)],
    [(DOTS, GREEN), (DOTS, GREEN), (DOTS, GREEN), ("w", GREEN), ("w", GREEN), ("w", GREEN), ("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
]

MAT_LEAKY = [  # image 24：Leaky ReRoPE 合并矩阵（红=窗口内取自 A，绿=窗口外按 w+k/t 递增）
    [("0", RED)],
    [("1", RED), ("0", RED)],
    [("2", RED), ("1", RED), ("0", RED)],
    [(DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w", GREEN), ("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w+1/t", GREEN), ("w", GREEN), (DOTS, RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
    [("w+2/t", GREEN), ("w+1/t", GREEN), (DOTS, GREEN), (DOTS, RED), (DOTS, RED), (DOTS, RED), (DOTS, RED)],
    [(DOTS, GREEN), ("w+2/t", GREEN), (DOTS, GREEN), (DOTS, GREEN), (DOTS, RED), (DOTS, RED), (DOTS, RED), (DOTS, RED)],
    [("w+(L-1-w)/t", GREEN), (DOTS, GREEN), (DOTS, GREEN), ("w+2/t", GREEN), ("w+1/t", GREEN), ("w", GREEN), ("w-1", RED), (DOTS, RED), ("2", RED), ("1", RED), ("0", RED)],
]


def draw_matrix(ax, rows: list, title: str) -> None:
    n_rows = len(rows)
    max_cols = max(len(r) for r in rows)
    row_h = 1.0
    col_w = 1.15

    for ri, row in enumerate(rows):
        y = -ri * row_h
        n = len(row)
        # 右对齐：该行最后一个元素固定落在最右列，往左依次错开（对应下三角结构）
        x_start = max_cols - n
        for ci, (text, color) in enumerate(row):
            x = (x_start + ci) * col_w
            fs = 8.3 if len(text) <= 3 else 7.0
            ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=color)

    x_left = -0.7 * col_w
    x_right = (max_cols - 1 + 0.7) * col_w
    y_top = 0.65 * row_h
    y_bot = -(n_rows - 1) * row_h - 0.65 * row_h
    # 用左右两条竖线 + 顶底小勾模拟大矩阵括号
    for x, sign in [(x_left, 1), (x_right, -1)]:
        ax.plot([x, x], [y_top, y_bot], color="#333333", linewidth=1.3)
        tick = 0.12 * col_w * sign
        ax.plot([x, x - tick], [y_top, y_top - 0.12], color="#333333", linewidth=1.3)
        ax.plot([x, x - tick], [y_bot, y_bot + 0.12], color="#333333", linewidth=1.3)

    ax.set_xlim(x_left - 0.5, x_right + 0.5)
    ax.set_ylim(y_bot - 0.5, y_top + 0.6)
    ax.set_title(title, fontsize=10.5, pad=8)
    ax.axis("off")


fig, axes = plt.subplots(2, 2, figsize=(11, 11.5), dpi=150)
draw_matrix(axes[0, 0], MAT_A, "① 矩阵 A（全局按真实间隔 1）")
draw_matrix(axes[0, 1], MAT_A_TILDE, "② 矩阵 Ã（全局按 1/t 缩放）")
draw_matrix(axes[1, 0], MAT_REROPE, "③a ReRoPE 合并矩阵\n（绿色窗口外恒为 w，完全封顶）")
draw_matrix(axes[1, 1], MAT_LEAKY, "③b Leaky ReRoPE 合并矩阵\n（绿色窗口外按 w+k/t 缓慢递增）")

fig.suptitle(
    "ReRoPE / Leaky ReRoPE 的两步合并：矩阵 A、Ã 与最终合并矩阵（红=窗口内取自 A，绿=窗口外）",
    fontsize=12.5, fontweight="bold", y=0.985,
)
fig.tight_layout(rect=[0, 0, 1, 0.955])
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
