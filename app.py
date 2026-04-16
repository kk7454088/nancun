import streamlit as st
import requests
import base64

# --- 1. 软件界面设置 ---
st.set_page_config(page_title="南村团队 AI 商业生图", layout="centered")
st.title("🎨 南村专属 AI 商业生图工作台 (直连版)")

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

st.sidebar.info("💡 采用原生底层 HTTP 协议，已精准匹配最新的 Nano Banana 2 (Gemini 3 Flash Image) 架构。")

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
        with st.spinner("正在通过底层通道直连 Google 渲染集群..."):
            # 融合高品质商业摄影指令和电商比例要求
            final_prompt = f"{prompt}, professional product photography, high definition, sharp focus, aspect ratio: {aspect_ratio}"
            
            # 【核心修复】：使用个人开发者 Key 专属的 Gemini 3.1 Flash Image Preview 接口
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"
            
            # 【核心修复】：使用标准的 Gemini 请求包格式
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
                # 直接发送网络请求
                response = requests.post(url, json=payload)
                
                # 如果请求成功 (状态码 200)
                if response.status_code == 200:
                    data = response.json()
                    image_found = False
                    
                    # 逐层扒开 Google 返回的“数据包”寻找图片
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        for part in parts:
                            if "inlineData" in part:
                                b64_img = part["inlineData"]["data"]
                                img_bytes = base64.b64decode(b64_img)
                                st.success("✅ 渲染完成！")
                                st.image(img_bytes, caption="南村团队专属生成结果", use_container_width=True)
                                image_found = True
                                break
                    
                    if not image_found:
                        st.warning("⚠️ 请求成功，但未返回图片（可能是您的提示词触发了人像或版权审核拦截）。")
                        with st.expander("点击查看原始服务器数据"):
                            st.json(data)
                            
                else:
                    # 如果请求失败，直接打印最真实的报错
                    st.error(f"❌ 渲染失败，HTTP 状态码: {response.status_code}")
                    st.info(f"服务器真实反馈: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ 网络通讯出现异常：{e}")
