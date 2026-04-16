import streamlit as st
import requests
import base64

# --- 1. 软件界面设置 ---
st.set_page_config(page_title="南村团队 AI 商业生图", layout="centered")
st.title("🎨 南村专属 AI 商业生图工作台 (2.5 兼容版)")

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

st.sidebar.info("💡 当前使用：Gemini 2.5 渲染引擎。已适配免费 API Key 额度。")

# --- 3. 画面描述 ---
st.markdown("### 📝 视觉画面描述")
prompt = st.text_area("请输入设计提示词：", height=150, placeholder="例如：一款极简风格的蝴蝶结耳环，放置在柔和光线的丝绒首饰盒中，4k 高画质商业摄影...")

# --- 4. 渲染逻辑 (底层 HTTP 直连) ---
if st.button("🚀 开始渲染商业大片", use_container_width=True):
    if not api_key:
        st.error("⚠️ 请先在左侧填入 API Key！")
    elif not prompt:
        st.error("⚠️ 提示词不能为空！")
    else:
        with st.spinner("正在通过 2.5 专属通道连接 Google 渲染集群..."):
            # 融合电商营销指令
            final_prompt = f"{prompt}, professional product photography, high definition, sharp focus, aspect ratio: {aspect_ratio}"
            
            # 【核心修复】：切换为 2.5 免费兼容版模型地址
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": final_prompt}
                        ]
                    }
                ]
            }
            
            try:
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    image_found = False
                    
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        for part in parts:
                            if "inlineData" in part:
                                b64_img = part["inlineData"]["data"]
                                img_bytes = base64.b64decode(b64_img)
                                st.success("✅ 渲染完成！")
                                st.image(img_bytes, caption="南村团队专属 2.5 生成结果", use_container_width=True)
                                image_found = True
                                break
                    
                    if not image_found:
                        st.warning("⚠️ 请求成功，但未返回图片（可能触发了安全审核拦截）。")
                        with st.expander("点击查看原始反馈数据"):
                            st.json(data)
                            
                elif response.status_code == 429:
                    st.error("❌ 触发频率限制 (429)。")
                    st.info("提示：免费版每分钟限制生成 2-5 次。请等待 1 分钟后再点击。")
                else:
                    st.error(f"❌ 渲染失败，HTTP 状态码: {response.status_code}")
                    st.info(f"服务器真实反馈: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ 网络通讯异常：{e}")
