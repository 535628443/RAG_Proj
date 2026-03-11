# 🩺 Diabetes-Expert-RAG: 糖尿病 AI 医学问诊系统

这是一个基于 **RAG (Retrieval-Augmented Generation, 检索增强生成)** 技术的本地医学咨询原型系统。项目通过集成大语言模型与专业医学指南，实现了 100% 本地化的专业问答能力。

## 🌟 项目亮点

- **100% 本地运行**：基于 Ollama 部署 DeepSeek-R1 与 BGE-M3，无需 API Key，保护隐私且零成本。
- **专业证据溯源**：基于 11 份权威糖尿病诊疗指南（PDF），回答内容均可追溯至原文。
- **现代化工程管理**：使用 `uv` 进行依赖管理，支持 Docker 容器化部署，确保环境一致性。
- **交互式 Web UI**：使用 Streamlit 搭建，提供流畅的类 ChatGPT 问答体验。

## 🛠️ 技术栈

- **LLM**: DeepSeek-R1 (1.5B)
- **Embedding**: BGE-M3 (针对中文医学优化)
- **Framework**: LangChain, LangChain-Chroma
- **Vector DB**: ChromaDB
- **UI**: Streamlit
- **Package Manager**: [uv](https://github.com/astral-sh/uv)

## 📂 项目结构

```text
RAG_Proj/
├── data/               # 数据存储
│   ├── documents/      # 原始医学指南 (PDF)
│   └── chroma_bge-m3/  # 持久化向量数据库
├── src/                # 源代码
│   ├── model_and_embedding.py  # 模型配置与嵌入逻辑
│   ├── update_database.py      # 数据入库与向量化脚本
│   ├── query_data.py           # RAG 核心检索逻辑
│   └── ui.py                   # Streamlit Web 界面
├── Dockerfile          # 容器化配置文件
├── pyproject.toml      # 项目元数据与依赖 (uv 格式)
└── requirements.txt    # 通用依赖清单 (pip 兼容)
```

## 🚀 快速开始

### 1. 环境准备
确保已安装 [Ollama](https://ollama.com/) 并下载所需模型：
```bash
ollama pull deepseek-r1:1.5b
ollama pull bge-m3
```

### 2. 初始化项目
使用 `uv` 自动同步依赖：
```bash
uv sync
```

### 3. 构建知识库 (首次运行)
将 PDF 指南放入 `data/documents/`，然后运行：
```bash
uv run src/update_database.py
```

### 4. 启动 Web 界面
```bash
uv run streamlit run src/ui.py
```

## 📝 开发者心得
本项目在复刻过程中，深入解决了 LangChain 版本迁移、ChromaDB 路径兼容性以及 PDF AES 解密等核心工程问题，是一次完整的从“数据处理”到“产品交付”的实战练习。

---
*本项目仅供学术研究与学习参考，不作为最终医学诊断建议。*
