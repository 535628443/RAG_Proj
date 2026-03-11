import argparse
# pathlib 替代了 os.path
from pathlib import Path
import shutil
#【搬运工】：专门负责读取一个文件夹里所有的PDF文件
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
#【切片刀】：最核心的工具，它能根据句号、换行，智能地把长文章切成一小块一小块
from langchain_text_splitters import RecursiveCharacterTextSplitter
#【纸片】：定义了“知识碎片”的长相，每一个碎片都包含“文字内容”和“元数据”
from langchain_core.documents import Document
#【仓库】：这是向量数据库 Chroma 的Python接口，它负责把切好的碎片存入本地磁盘
from langchain_community.vectorstores.chroma import Chroma
#【大脑核心】：引入 model_and_embedding.py 中写的函数和配置
from model_and_embedding import get_embedding_function, EMBEDDING_NAME

# --- 路径配置 --- 
# os.path 的写法
""" 
os.path可以让代码在不同操作系统上都能正确处理文件路径(比如Windows和Linux的路径分隔符不同)
DATASET_PATH = os.path.join("data", f"chroma_{EMBEDDING_NAME}")
DOCUMENT_PATH = os.path.join("data", "documents") 
"""

# pathlib 的写法
DATASET_PATH = Path("data") / f"chroma_{EMBEDDING_NAME}"
DOCUMENT_PATH = Path("data") / "documents"

def main():
    parser = argparse.ArgumentParser() # 听候终端上输入的指令
    parser.add_argument("--reset",
                        action="store_true",
                        help="是否重新构建数据库, 默认是False") 
    # -- 表示可选参数, 定义了按钮的名字(reset), 没有--表示位置参数(必须填)
    # action 表示命令行出现了 arts.reset 就把 args.reset 设为True,(默认为False) 
    # help 表示 --reset 的说明书
    args = parser.parse_args() 
    # .parse_args() 会自动识别命令行输入的参数, 比如你输入了 --reset, 
    # 那么 args.reset 就是 True; 如果你没有输入 --reset, 那么 args.reset 就是 False

    if args.reset:
        clear_database()

    # 1. 加载文档
    documents = load_documents()
    # 2. 切分文档
    chunks = split_documents(documents)
    # 3. 存入数据库
    add_to_chroma(chunks)

def clear_database():
    """删除旧的数据库文件夹，清空之前的知识库"""
    if DATASET_PATH.exists():
        print(f"✨ 正在清理旧数据库：{DATASET_PATH}")
        shutil.rmtree(DATASET_PATH) # 删除整个文件夹

def load_documents():
    """读取 data/documents下所有的PDF文件"""
    print(f"📂 正在加载文档：{DOCUMENT_PATH}")
    loader = PyPDFDirectoryLoader(DOCUMENT_PATH) 
    # PyPDFDirectoryLoader 可以读取目录下所有PDF文件的地址
    return loader.load() 
    # .load() 会根据地址对PDF进行操作, 变成 Document 对象, 并返回一个 list[Document] 结构

def split_documents(documents: list[Document]):
    #documents: list[Document] 表示这个函数的输入是一个 Document 对象的列表(冒号表示注解)
    """
    Document(
    page_content="糖尿病患者应注意控制糖分摄入, 建议每日运动30分钟...", 
    metadata={
        'source': 'data/source/中国2型糖尿病防治指南.pdf', 
        'page': 45
    }
    )
    """
    """把长文档切成1000字上下的片段, overlap 是为了让片段之间有200字的重复, 防止语义在切分点被切断"""
    print("🔪 正在切分文档...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        add_start_index=True)
    # chunk_size 是每个碎片的最大长度
    # chunk_overlap 是碎片之间的重叠部分(为了保持上下文连续)
    # add_start_index=True 记录碎片在原文中的起始位置(比如碎片从第二页第101个字符开始)
    
    return text_splitter.split_documents(documents)
    # 1. 循环遍历这个 list[Document]，对每个 Document 进行切分
    # 2. 读取它的 .page_content
    # 3. 按照 1000 字一段进行split, 每段之间重叠 200 字
    # 4. 对每个切好的碎片，创建一个新的 Document 对象
    # 5. 在新的 Document 对象的 metadata 中，记录原文档的 metadata 和这个碎片在原文中的起始位置
    # 6. 最后返回一个新的 list[Document]，里面的每个 Document 都是一个切好的碎片

def add_to_chroma(chunks: list[Document]):
    """把切好的碎片存入 Chroma 数据库"""
    print("💾 正在存储到 Chroma 数据库...")
    db = Chroma(
        persist_directory=str(DATASET_PATH),
        embedding_function=get_embedding_function()
    )

    db.add_documents(chunks) # 把所有chunks发给bge-m3, 让它把每个chunk变成一个向量, 然后存入数据库(内存中)
    db.persist() # 保存数据库的内容到磁盘(否则会丢失)
    print(f"✅ 已成功将 {len(chunks)} 个知识碎片存入数据库：{DATASET_PATH}")

if __name__ == "__main__": # 有这段才能在终端运行 python src/update_database.py 
    main()