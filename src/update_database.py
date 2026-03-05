import argparse
import os
import shutil
#【搬运工】：专门负责读取一个文件夹里所有的PDF文件
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
#【切片刀】：最核心的工具，它能根据句号、换行，智能地把长文章切成一小块一小块
from langchain_text_splitters import RecursiveCharacterTextSplitter
#【纸片】：定义了“知识碎片”的长相，每一个碎片都包含“文字内容”和“元数据”
from langchain.schema.document import Document
#【仓库】：这是向量数据库 Chroma 的Python接口，它负责把切好的碎片存入本地磁盘
from langchain_community.vectorstores.chroma import Chroma
#【大脑核心】：引入 model_and_embedding.py 中写的函数和配置
from model_and_embedding import get_embedding_function, EMBEDDING_NAME

