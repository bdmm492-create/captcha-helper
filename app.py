import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
from ultralytics import YOLO

st.set_page_config(page_title="CAPTCHA Solver", layout="centered")

st.title("🤖 All-in-One CAPTCHA Solver")
st.write("টেক্সট ক্যাপচা (Text CAPTCHA) এবং ইমেজ অবজেক্ট ক্যাপচা (Visual Grid CAPTCHA) উভয়ই প্রসেস করতে নিচে ছবি আপলোড করুন।")

# Load YOLO Model (Visual CAPTCHA detection)
@st.cache_resource
def load_yolo():
    return YOLO('yolov8n.pt')

yolo_model = load_yolo()

# File Uploader
uploaded_file = st.file_uploader("ক্যাপচা ছবি আপলোড করুন", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Read Image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("মূল ছবি")
        st.image(image, use_column_width=True)

    st.markdown("---")
    st.subheader("🔍 ফলাফল")

    # 1. YOLO Object Detection Analysis
    results = yolo_model(img_array)
    res_plotted = results[0].plot()

    st.write("### ১. অবজেক্ট ডিটেকশন (YOLO):")
    st.image(res_plotted, caption="ডিটেক্ট করা অবজেক্টসমূহ", use_column_width=True)

    # 2. Text Extraction (OCR)
    st.write("### ২. টেক্সট এক্সট্রাকশন (OCR):")
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    extracted_text = pytesseract.image_to_string(gray).strip()
    
    if extracted_text:
        st.success(f"খুঁজে পাওয়া টেক্সট: **{extracted_text}**")
    else:
        st.info("ছবিতে কোনো পরিষ্কার টেক্সট পাওয়া যায়নি।")
