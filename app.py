import streamlit as st
from google import genai
from google.genai import types
import base64

# --- 1. 软件界面设置 ---
st.set_page_config(page_title="南村团队 AI 商业生图", layout="centered")
st.title("🎨 南村专属 AI 商业生图工作台 (官方同步版)")

# --- 2. 侧边栏配置 ---
st.sidebar.header("🔑 核心配置")
api_key = st.sidebar.text_input("在此输入您的 Google API Key", type="password")

st.sidebar.markdown("---")
# 对应官方代码中的 aspect_ratio 设置
size_options = {
    "1:1 (正方形主图)": "1:1",
    "3:4 (饰品详情图)": "3:4",
    "9:16 (TikTok 竖屏)": "9:16"
}
selected_label = st.sidebar.selectbox("选择图片尺寸比例", list(size_options.keys()))
aspect_ratio = size_options[selected_label]

# --- 3. 画面描述 ---
st.markdown("### 📝 视觉画面描述")
prompt = st.text_area("请输入设计提示词：", height=150, placeholder="例如：蝴蝶结耳环，极简风格，商业摄影...")

# --- 4. 生成逻辑 (完全同步官方 SDK) ---
if st.button("🚀 开始渲染商业大片", use_container_width=True):
    if not api_key:
        st.error("⚠️ 请先在左侧填入 API Key！")
    elif not prompt:
        st.error("⚠️ 提示词不能为空！")
    else:
        with st.spinner("正在呼叫官方 Gemini 2.5 渲染引擎..."):
            try:
                # 初始化官方 Client
                client = genai.Client(api_key=api_key)
                
                # 配置生成参数 (对应你截图中的 GenerateContentConfig)
                generate_content_config = types.GenerateContentConfig(
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        person_generation="ALLOW_ADULT", # 放宽审核
                    ),
                    response_modalities=["IMAGE"],
                )

                # 调用模型 (使用你截图中确认的 gemini-2.5-flash-image)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=prompt,
                    config=generate_content_config,
                )

                # 提取图片数据
                image_found = False
                for chunk in response:
                    if chunk.parts:
                        for part in chunk.parts:
                            if part.inline_data:
                                img_data = part.inline_data.data
                                # 如果返回的是 bytes 类型直接显示，否则解码
                                if isinstance(img_data, bytes):
                                    st.image(img_data, caption="南村团队专属渲染结果", use_container_width=True)
                                else:
                                    st.image(base64.b64decode(img_data), caption="南村团队专属渲染结果", use_container_width=True)
                                st.success("✅ 渲染完成！")
                                image_found = True
                
                if not image_found:
                    st.warning("⚠️ 未检测到生成的图片数据，可能触发了内容审核。")

            except Exception as e:
                st.error(f"❌ 渲染失败。错误详情：{e}")
                st.info("💡 如果依然报错 429，说明免费 API Key 暂不支持该模型的外部调用，建议在 AI Studio 开启 Billing 升级。")
