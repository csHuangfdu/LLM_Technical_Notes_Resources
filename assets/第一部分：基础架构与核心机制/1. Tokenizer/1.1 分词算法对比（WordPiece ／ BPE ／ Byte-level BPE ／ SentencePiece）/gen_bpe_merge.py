import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.1 分词算法对比（WordPiece ／ BPE ／ Byte-level BPE ／ SentencePiece）/bpe-merge.png"

# 经典 BPE 训练实例（语料: low=5, lower=2, newest=6, widest=3）
# 初始符号集: {l,o,w,e,r,n,s,t,i,d, </w>} = 11
header = ["Iter", "Top pair (by freq)", "New symbol", "Vocab size"]
rows = [
    ["0", "(initial char vocab + </w>)", "-", "11"],
    ["1", "(e, s)  freq=9", "es", "12"],
    ["2", "(es, t) freq=9", "est", "13"],
    ["3", "(t, </w>) freq=9", "t</w>", "14"],
    ["4", "(w, e)  freq=8", "we", "15"],
    ["5", "(l, o)  freq=7", "lo", "16"],
]

fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
ax.axis("off")
tbl = ax.table(
    cellText=rows,
    colLabels=header,
    colWidths=[0.08, 0.42, 0.22, 0.18],
    loc="center",
    cellLoc="center",
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 1.7)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#2f4b7c")
        cell.set_text_props(color="white", weight="bold")
    else:
        cell.set_facecolor("#f2f5fa" if r % 2 else "white")
    cell.set_edgecolor("#c9d2e0")

ax.set_title(
    "BPE worked example: iterative merge on {low:5, lower:2, newest:6, widest:3}",
    fontsize=12, weight="bold", pad=12,
)
fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
print("saved", OUT)
