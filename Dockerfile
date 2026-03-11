# --- 第一阶段：环境准备 ---
# 使用轻量级 Python 3.11 镜像
FROM python:3.11-slim

# 安装 uv (当前最快的 Python 包管理工具)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# 禁用字节码生成（让镜像更干净）
ENV PYTHONDONTWRITEBYTECODE=1
# 禁用输出缓冲（让日志能实时显示在终端）
ENV PYTHONUNBUFFERED=1

# --- 第二阶段：安装依赖 ---
# 先复制依赖清单，利用 Docker 的缓存机制
COPY pyproject.toml uv.lock ./

# 使用 uv 同步环境 (不创建虚拟环境，直接装在系统目录下)
RUN uv sync --frozen --no-cache

# --- 第三阶段：复制项目内容 ---
# 复制源代码
COPY src/ ./src/
# 复制数据（包括你入库好的向量数据库和原始 PDF）
COPY data/ ./data/

# --- 第四阶段：配置运行环境 ---
# 暴露 Streamlit 默认端口
EXPOSE 8501

# 设置 Streamlit 运行参数：监听所有网卡
CMD ["uv", "run", "streamlit", "run", "src/ui.py", "--server.address=0.0.0.0", "--server.port=8501"]
