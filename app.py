import streamlit as st
from PIL import Image
from ultralytics import YOLO

st.set_page_config(page_title="CAPTCHA Solver", layout="centered")

st.title("🤖 CAPTCHA Object Detector")
st.write("ক্যাপচা ছবি আপলোড করলে YOLOv8 মডেল স্বয়ংক্রিয়ভাবে অবজেক্টসমূহ চিহ্নিত করে দেবে।")

# Load YOLO Model
@st.cache_resource
def load_yolo():
    return YOLO('yolov8n.pt')

model = load_yolo()

# File Uploader
uploaded_file = st.file_uploader("ক্যাপচা ছবি আপলোড করুন", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.subheader("মূল ছবি")
    st.image(image, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 ডিটেকশন ফলাফল")

    with st.spinner("ছবি প্রসেস করা হচ্ছে..."):
        results = model(image)
        res_plotted = results[0].plot()

    st.image(res_plotted, caption="ডিটেক্ট করা অবজেক্টসমূহ", use_container_width=True)
