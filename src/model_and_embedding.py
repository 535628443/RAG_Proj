
import os
import dotenv
from langchain_ollama import OllamaEmbeddings

# 强制绕过代理
os.environ["no_proxy"] = "localhost,127.0.0.1"
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# 加载 .env 配置
dotenv.load_dotenv(verbose=True)

# --- 配置区 ---
OLLAMA_MODEL_NAME = "deepseek-r1:1.5b"
OLLAMA_EMBEDDING_NAME = "bge-m3"

# --- 逻辑区 ---
def get_embedding_function():
    """返回本地 Ollama (BGE-M3) 的向量嵌入工具"""
    return OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_NAME
    )

EMBEDDING_NAME = OLLAMA_EMBEDDING_NAME
