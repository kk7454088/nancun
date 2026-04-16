import streamlit as st
import google.generativeai as genai

# === 1. 软件界面全局设置 ===
st.set_page_config(page_title="南村团队 AI 商业视觉助手", layout="centered")
st.title("🎨 南村专属 AI 商业生图工作台 (公网版)")

# === 2. 侧边栏：电商参数配置 ===
st.sidebar.header("🔑 核心配置")
api_key = st.sidebar.text_input("在此输入您的 Google API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📐 输出规格")
size_map = {
    "1:1 (亚马逊主图/白底图)": "1:1",
    "9:16 (TikTok 视频封面/短视频)": "9:16",
    "16:9 (横版品牌海报)": "16:9"
}
selected_size_label = st.sidebar.selectbox("选择图片尺寸比例", list(size_map.keys()))
aspect_ratio = size_map[selected_size_label]

st.sidebar.info("💡 提示：部署在云端无需配置代理，速度极快。")

# === 3. 主操作区：Prompt 输入 ===
st.markdown("### 📝 视觉画面描述")
prompt = st.text_area(
    "请输入您的设计提示词：", 
    height=150,
    placeholder="例如：一款极简风格的蝴蝶结耳环，放置在柔和光线的丝绒首饰盒中，4k 高画质商业摄影..."
)

# === 4. 核心生成逻辑 ===
if st.button("🚀 开始渲染商业大片", use_container_width=True):
    if not api_key:
        st.error("⚠️ 请先在左侧填入 API Key！")
    elif not prompt:
        st.error("⚠️ 提示词不能为空！")
    else:
        with st.spinner("云端模型正在全速渲染中..."):
            try:
                # 在云端部署，直接配置即可，无需 transport='rest' 也能跑通
                genai.configure(api_key=api_key)
                
                # 融合电商营销参数
                final_prompt = f"{prompt}, aspect ratio: {aspect_ratio}, professional product photography, high definition"
                
                # 调用 Gemini 生图模型
                model = genai.GenerativeModel('gemini-3-flash-image')
                response = model.generate_content(final_prompt)
                
                # 检查并展示渲染结果
                image_found = False
                for part in response.parts:
                    if hasattr(part, 'inline_data'):
                        st.success("✅ 商业视觉渲染完成！")
                        st.image(part.inline_data.data, caption="南村团队专属 AI 生成结果", use_container_width=True)
                        image_found = True
                
                if not image_found:
                    st.warning("⚠️ 生成未包含图片。可能触发了安全拦截（如人像审核）。")
                    if response.text:
                        st.info(f"模型反馈信息：{response.text}")
                    
            except Exception as e:
                st.error(f"❌ 渲染失败，错误详情：{e}")