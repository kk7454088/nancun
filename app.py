import streamlit as st
from google import genai
from google.genai import types

# --- 1. 软件界面设置 ---
st.set_page_config(page_title="南村团队 AI 商业生图", layout="centered")
st.title("🎨 南村专属 AI 商业生图工作台 (公网版)")

# --- 2. 侧边栏配置 ---
st.sidebar.header("🔑 核心配置")
api_key = st.sidebar.text_input("在此输入您的 Google API Key", type="password")

st.sidebar.markdown("---")
size_map = {
    "1:1 (亚马逊主图/白底图)": "1:1",
    "9:16 (TikTok 视频/封面)": "9:16",
    "16:9 (横版品牌海报)": "16:9"
}
selected_size_label = st.sidebar.selectbox("选择图片尺寸比例", list(size_map.keys()))
aspect_ratio = size_map[selected_size_label]

# --- 3. 画面描述 ---
st.markdown("### 📝 视觉画面描述")
prompt = st.text_area("请输入设计提示词：", height=150, placeholder="例如：蝴蝶结耳环，极简风格，商业摄影...")

# --- 4. 渲染逻辑 ---
if st.button("🚀 开始渲染商业大片", use_container_width=True):
    if not api_key:
        st.error("⚠️ 请先在左侧填入 API Key！")
    elif not prompt:
        st.error("⚠️ 提示词不能为空！")
    else:
        with st.spinner("云端模型正在全速渲染中..."):
            try:
                # 使用最新版 Google GenAI 客户端
                client = genai.Client(api_key=api_key)
                
                # 融合高品质商业摄影指令
                final_prompt = f"{prompt}, professional product photography, high definition, sharp focus"
                
                # 调用公网 Imagen 模型
                response = client.models.generate_images(
                    model='imagen-3.0-generate-001',
                    prompt=final_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio=aspect_ratio,
                    )
                )
                
                if response.generated_images:
                    st.success("✅ 渲染完成！")
                    img_bytes = response.generated_images[0].image.image_bytes
                    st.image(img_bytes, caption="南村团队专属生成结果", use_container_width=True)
                else:
                    st.warning("⚠️ 渲染成功但未返回图片，可能是提示词触发了安全拦截。")
            except Exception as e:
                st.error(f"❌ 渲染失败，请检查 API Key 或网络环境。详情：{e}")
