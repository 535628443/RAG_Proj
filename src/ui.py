import streamlit as st
import os
from query_data import query_rag

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="糖尿病AI医学助手",
    page_icon="🩺",
    layout="wide"
)

# --- 2. 界面样式定制 ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .source-box {
        background-color: #e3f2fd;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
        border-left: 5px solid #2196f3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 侧边栏：关于和设置 ---
with st.sidebar:
    st.title("🩺 糖尿病助手")
    st.info("本助手基于 **DeepSeek-R1** 和 **11份官方医学指南** 构建，仅供学习参考，不作为最终诊断建议。")
    
    if st.button("清除聊天记录"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("技术栈: LangChain + ChromaDB + Ollama")

# --- 4. 聊天记录状态初始化 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. 渲染历史消息 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 查看参考来源"):
                for src in message["sources"]:
                    st.write(f"- {os.path.basename(src)}")

# --- 6. 输入框逻辑 ---
if prompt := st.chat_input("您可以问我关于糖尿病的任何问题，例如：'糖尿病患者能吃西瓜吗？'"):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 显示 AI 思考和回答
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 正在查阅医学资料并思考中...")
        
        try:
            # 调用我们之前的后台逻辑
            response, sources = query_rag(prompt)
            # query_rag 返回的tuple会被unpack然后依次赋值给两个变量
            
            # 渲染回答
            message_placeholder.markdown(response)
            
            # 渲染来源（如果存在）
            if sources:
                with st.expander("📚 本次回答参考了以下资料"):
                    for src in sources:
                        st.write(f"- {os.path.basename(src)}")
            
            # 保存到记录
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })
            
        except Exception as e:
            st.error(f"❌ 运行出错了: {str(e)}")
            message_placeholder.empty()

