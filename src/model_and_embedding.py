import os
import dotenv
from langchain_community.embeddings.ollama import OllamaEmbeddings
os.environ["no_proxy"] = "localhost,127.0.0.1"
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# 加载 .env 文件（如果你以后有 API Key，可以放在 .env 里）
dotenv.load_dotenv(verbose=True) # 明确告诉你它正在尝试从哪个路径加载 .env 文件, False会静默

# --- 配置区 ---
OLLAMA_MODEL_NAME = "deepseek-r1:1.5b" # 对话模型
OLLAMA_EMBEDDING_NAME = "bge-m3"       # 向量嵌入模型

# 默认使用 Ollama 作为提供商
EMBEDDING_PROVIDER = "Ollama"

# --- 逻辑区 ---
def get_embedding_function():
    """返回本地 Ollama 的嵌入工具"""
    return OllamaEmbeddings(
        model = OLLAMA_EMBEDDING_NAME,
        embed_instruction = "文档：",
        query_instruction = "询问：",
    )
    """bge-m3在处理“知识库里的文字”和“用户问的问题”时
    加上这两个前缀，它能更精准地把“问题”和“知识”匹配在一起"""

EMBEDDING_NAME = OLLAMA_EMBEDDING_NAME