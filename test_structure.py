
import os
from langchain_chroma import Chroma
from src.model_and_embedding import get_embedding_function

def test_structure():
    CHROMA_PATH = "data/chroma_bge-m3"
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embedding_function)
    
    query = "糖尿病吃西瓜"
    print(f"\n--- 测试 similarity_search_with_score ---")
    results = db.similarity_search_with_score(query, k=1)
    print(f"结果类型: {type(results)}")
    if len(results) > 0:
        first_item = results[0]
        print(f"第一项类型: {type(first_item)}")
        print(f"第一项内容: {first_item}")
        for i, val in enumerate(first_item):
            print(f"  索引 {i} 的类型: {type(val)}")

    print(f"\n--- 测试 similarity_search ---")
    docs = db.similarity_search(query, k=1)
    print(f"结果类型: {type(docs)}")
    if len(docs) > 0:
        print(f"第一项类型: {type(docs[0])}")

if __name__ == "__main__":
    test_structure()
