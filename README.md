# LLM_Technical_Notes_Resources（公开资源仓库）

本仓库是 **LLM 技术笔记** 系统的**公开资源镜像**，被核心私有仓库
[`LLM_Technical_Notes`](https://github.com/csHuangfdu/LLM_Technical_Notes)
以 **git submodule** 形式引入（目录名即本仓库名）。

Notion **只能访问公开仓库**里的图片，因此所有图片等二进制资源都放在这里，
核心代码逻辑留在私有仓库，互不泄露。

## 目录结构（与 Notion 页面树 1:1 对应，按「节」独立目录）

每个「节」（如 1.1）在 Notion 中都是独立页面，配套有**专属资源目录**：

```text
assets/
├── 第一部分：基础架构与核心机制/                          <- 对应 Notion「部分」页
│   ├── 1. Tokenizer/                                      <- 对应 Notion「章」页
│   │   ├── 1.1 分词算法对比（WordPiece ／ BPE ／ Byte-level BPE ／ SentencePiece）/   <- 对应 Notion「节」页
│   │   │   └── bpe-merge.png    <- 文件名直接用含义命名，不必再加节编号前缀
│   │   └── 1.2 词表大小选择与性能影响/
│   └── 2. 位置编码/
│       └── 2.2 旋转位置编码（RoPE）原理与实现/
└── 第二部分：训练与对齐/
    └── 7. 预训练/
        └── ...
```

- 目录名中的 `/` 已替换为全角 `／`（文件系统限制），与 Notion 页面标题原文不同，
  但一一对应，替换规则见核心仓 `src/build_outline.py` 的 `safe_name()`。
- 若某节的子节也独立成页（4 级页面），资源目录再深一层：`.../<节>/<子节>/`。
- 目录按需创建（有图片才建），不再预置大量空 `.gitkeep` 占位目录。

## 图片如何被 Notion 加载

核心仓库的 `src/build_outline.py` 在 `--sync` 时，把节 `.md` 文件里的
`![说明](assets/<部分>/<章>/<节>/x.png)` 直接拼接为：

```
https://raw.githubusercontent.com/csHuangfdu/LLM_Technical_Notes_Resources/main/assets/<部分>/<章>/<节>/x.png
```

即**图片完全由 md 中的显式引用决定**，不再有"按文件名节编号自动发现"的机制——
每节有自己的目录，路径本身就唯一确定归属，不需要额外映射。

## 工作流（在核心私有仓库内操作）

```bash
# 1) 放入图片（目录对齐节，无需编号前缀命名）
mkdir -p "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.1 分词算法对比（WordPiece ／ BPE ／ Byte-level BPE ／ SentencePiece）"
cp my_fig.png "LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.1 分词算法对比（WordPiece ／ BPE ／ Byte-level BPE ／ SentencePiece）/my_fig.png"

# 2) 进入 submodule 提交并推送到公开仓库
cd LLM_Technical_Notes_Resources
git add assets/ && git commit -m "add tokenizer figure" && git push origin main
cd ..

# 3) 在对应节的 .md 里插入引用（带 assets/ 前缀），然后同步到 Notion
PYTHONPATH=src python3 src/build_outline.py --sync

# 4)（可选）把 submodule 指针变化提交回核心私有仓库
git add LLM_Technical_Notes_Resources && git commit -m "bump resources" && git push origin main
```

## 注意事项

- 本仓库须保持 **Public**，Notion 才能加载 `raw.githubusercontent.com` 上的图片。
- 默认分支名（`main`/`master`）须与核心仓 `REPO_RAW_BASE` 中写的一致。
- 本地若把资源仓克隆在别处，可设置环境变量 `NOTION_ASSETS_ROOT` 指向其
  `assets/` 目录（供脚本内部工具函数使用）。
- md 引用路径必须**带** `assets/` 前缀（相对资源仓根目录，不是相对 `assets/` 目录本身），
  且路径中的 `/` 要换成全角 `／` 与实际目录名一致，否则图片会 404 不显示。
