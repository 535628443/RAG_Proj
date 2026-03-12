import streamlit as st
import os
import time
from query_data import query_rag

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="糖尿病AI医学助手",
    page_icon="🩺",
    layout="centered", # 居中布局更类似 ChatGPT 的现代排版，阅读更护眼
    initial_sidebar_state="expanded"
)

# --- 2. 现代感界面与双端兼容 CSS ---
st.markdown("""
    <style>
    /* 布局微调 */
    .block-container {
        padding-top: 3.5rem; /* 增加顶部留白，避免标题遮挡 */
        padding-bottom: 4rem;
    }
    /* 现代感渐变标题容器与排版 */
    .title-wrapper {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        padding-top: 10px; /* 防止内容顶部被容器裁剪 */
    }
    .title-emoji {
        font-size: 2.6rem;
    }
    .title-text {
        background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.6rem;
        letter-spacing: -0.02rem;
    }
    /* 副标题样式，利用 Streamlit 本地变量自适应深浅色 */
    .subtitle-text {
        font-size: 1.1rem;
        color: var(--text-color);
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }
    /* 隐藏底部默认的 streamlit 标记，使界面更干净 */
    footer {visibility: hidden;}

    /* 彻底锁定侧边栏宽度并禁用调整 */
    [data-testid="stSidebar"] {
        min-width: 340px !important;
        max-width: 340px !important;
    }
    [data-testid="stSidebarResizer"] {
        display: none !important;
        pointer-events: none !important;
        width: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 侧边栏：关于和设置 ---
with st.sidebar:
    # 使用带有内联居中样式的 HTML 确保图标和标题完美居中展示，并调大尺寸
    st.markdown('''
        <div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
            <img src="https://cdn-icons-png.flaticon.com/512/3063/3063206.png" width="110">
            <h2 style="margin-top: 20px; margin-bottom: 0; font-size: 1.6rem; font-weight: 800;">🩺 糖尿病管理专家</h2>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('''
        <div style="background-color: rgba(33, 150, 243, 0.1); border-left: 4px solid #2196f3; padding: 12px; border-radius: 4px; margin-bottom: 15px;">
            <div style="display: flex; align-items: flex-start; gap: 8px;">
                <span style="font-size: 1.1em; line-height: 1.2;">🟢</span>
                <div>
                    <strong style="font-size: 0.9em; display: block; margin-bottom: 2px;">系统状态：在线</strong>
                    <span style="font-size: 0.85em; opacity: 0.85;">已成功连接本地医学指南库。</span>
                </div>
            </div>
        </div>
        
        <div style="background-color: rgba(255, 152, 0, 0.1); border-left: 4px solid #ff9800; padding: 12px; border-radius: 4px;">
            <div style="display: flex; align-items: flex-start; gap: 8px;">
                <span style="font-size: 1.1em; line-height: 1.2;">⚠️</span>
                <div>
                    <strong style="font-size: 0.9em; display: block; margin-bottom: 2px;">免责声明</strong>
                    <span style="font-size: 0.85em; opacity: 0.85;">本系统回答仅供参考，切勿替代专业医师的当面诊断与处方。</span>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("✨ 开启新对话", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("⚡ Powered by LangChain, ChromaDB & Ollama")

# --- 主页面头部 ---
st.markdown('<div class="title-wrapper"><span class="title-emoji">🏥</span><span class="title-text">糖尿病AI健康咨询</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">基于 DeepSeek-R1 与权威医学指南，为您提供专业、可信靠的健康解答。</div>', unsafe_allow_html=True)
st.divider()

# --- 渲染头像映射 ---
avatars = {"user": "🧑‍💻", "assistant": "🧑‍⚕️"}

# --- 4. 聊天记录状态初始化 ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "您好！我是您的专属糖尿病管理助手。请问今天有什么我可以帮您的？\n\n💡 **您可以试着这样问我：**\n- *“二型糖尿病患者早餐应该怎么吃？”*\n- *“空腹血糖8.5严重吗？”*\n- *“服用二甲双胍需要注意什么副作用？”*"
    }]

# --- 5. 渲染历史消息 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars.get(message["role"], "🤖")):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 参考指南来源"):
                for src in message["sources"]:
                    st.caption(f"🔗 `{os.path.basename(src)}`")

# --- 6. 输入框逻辑 ---
if prompt := st.chat_input("输入您关心的问题 (例如：'糖尿病患者能吃西瓜吗？')"):
    
    # 存入并显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatars["user"]):
        st.markdown(prompt)

    # 显示 AI 回答
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        
        # 使用 st.status 提供更友好的等待状态动画
        with st.status("🧠 正在检索本地权威医学知识库...", expanded=True) as status:
            st.write("🔎 正在提取问题特征并进行向量匹配...")
            try:
                # 调用原始查询逻辑
                response, sources = query_rag(prompt)
                status.update(label="✅ 检索与思考完成", state="complete", expanded=False)
                is_success = True
            except Exception as e:
                status.update(label="❌ 处理遭遇异常", state="error", expanded=True)
                st.error(f"失败详情: {str(e)}")
                is_success = False

        # --- 退出 status 块后，再显示回答，防止内容被折叠隐藏 ---
        if is_success:
            # 渲染最终回答
            st.markdown(response)
            
            # 渲染来源
            if sources:
                with st.expander("📚 决策参考来源"):
                    for src in sources:
                        st.caption(f"🔗 `{os.path.basename(src)}`")
                        
            # 存入历史记录
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })

