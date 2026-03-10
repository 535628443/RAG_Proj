import argparse
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from model_and_embedding import get_embedding_function

# 数据库路径
CHROMA_PATH = "data/chroma_bge-m3"

PROMPT_TEMPLATE = """
你是一位专业的糖尿病医生。请根据以下提供的医学背景信息来回答患者的问题。
如果背景信息中没有提到相关内容，请诚实告知，不要胡乱编造。

背景信息：{context}

---

患者的问题：{question}

请给出专业、易懂且有温度的回答：
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="你的问题")
    args = parser.parse_args()
    query_rag(args.query_text)

def query_rag(query_text: str):
    # 1. 初始化数据库
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embedding_function)

    # 2. 执行搜索
    docs = db.similarity_search(query_text, k=5)

    if not docs:
        print("❌ 未能在本地知识库中找到相关信息。")
        return

    # 3. 提取内容和来源
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "未知来源") for doc in docs]
    
    # 4. 构造 Prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # 5. 调用 Ollama (DeepSeek)
    model = OllamaLLM(model="deepseek-r1:1.5b")
    
    print("\n⏳ 正在思考中，请稍候...")
    response_text = model.invoke(prompt)

    # 6. 打印并返回结果
    unique_sources = list(set(sources))
    print(f"\n🤖 DeepSeek 的回答：\n{response_text}")
    print(f"\n🔖 参考来源：{unique_sources}")
    
    return response_text, unique_sources

if __name__ == "__main__":
    main()
