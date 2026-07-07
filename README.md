# LLM_Technical_Notes_Resources（公开资源仓库）

本仓库是 **LLM 技术笔记** 系统的**公开资源镜像**，被核心私有仓库
[`LLM_Technical_Notes`](https://github.com/csHuangfdu/LLM_Technical_Notes)
以 **git submodule** 形式引入（目录名即本仓库名）。

Notion **只能访问公开仓库**里的图片，因此所有图片等二进制资源都放在这里，
核心代码逻辑留在私有仓库，互不泄露。

## 目录结构（与 Notion 大纲 1:1 对应）

```text
assets/
├── 第一部分：基础架构与核心机制/      <- 对应 Notion「部分」页
│   ├── 1. Tokenizer/                  <- 对应 Notion「章」页
│   │   ├── 1.1 分词算法对比.png        <- 文件名以「节编号」开头
│   │   └── 1.2 词表大小选择与性能影响.png
│   └── 2. 位置编码/
│       └── 2.2 RoPE.png
└── 第二部分：训练与对齐/
    └── 7. 预训练/
        └── ...
```

空目录用 `.gitkeep` 占位，确保层级能被 Git 跟踪。

## 自动同步机制（无需手写映射）

核心仓库的 `src/build_outline.py` 会：

1. 遍历 `assets/` 下所有图片；
2. 提取文件名开头的「节编号」（如 `1.1`、`2.2`）；
3. 与大纲 MD 中的节标题匹配，把图片插到 Notion 对应节；
4. 子节图片（如 `1.1.1 细节.png`）自动挂到所属节 `1.1`。

日常用法：把图片按「正确目录 + 编号开头命名」放入 `assets/`，
push 后重跑构建即可，无需改任何配置文件。

## 工作流（在核心私有仓库内操作）

```bash
# 1) 放入图片（目录与命名对齐大纲）
cp my_fig.png LLM_Technical_Notes_Resources/assets/第一部分：基础架构与核心机制/1. Tokenizer/1.1 分词算法对比.png

# 2) 进入 submodule 提交并推送到公开仓库
cd LLM_Technical_Notes_Resources
git add assets/ && git commit -m "add tokenizer figure" && git push origin main
cd ..

# 3) 重新构建（自动发现图片并插入 Notion 对应节）
PYTHONPATH=src python3 src/build_outline.py --beautify

# 4)（可选）把 submodule 指针变化提交回核心私有仓库
git add LLM_Technical_Notes_Resources && git commit -m "bump resources" && git push origin main
```

## 显式覆盖（可选）

若需引用仓库外 URL，或覆盖自动发现结果，在核心仓库 `data/images.yaml` 写：

```yaml
3.2 注意力机制（QKV 含义、缩放因子、多头注意力）: https://example.com/attention.png
```

显式条目优先于自动发现。

## 注意事项

- 本仓库须保持 **Public**，Notion 才能加载 `raw.githubusercontent.com` 上的图片。
- 默认分支名（`main`/`master`）须与 `REPO_RAW_BASE` 中写的一致。
- 本地若把资源仓克隆在别处，可设置环境变量 `NOTION_ASSETS_ROOT` 指向其
  `assets/` 目录，脚本会据此生成 raw URL。
