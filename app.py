import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance

st.set_page_config(page_title="CAPTCHA Solver", layout="centered")

st.title("🧩 CAPTCHA Enhancement Tool")
st.write("ক্যাপচা ছবি আরও স্পষ্ট দেখতে নিচে আপলোড করুন।")

uploaded_file = st.file_uploader("ক্যাপচা ছবি আপলোড করুন", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.subheader("📸 মূল ছবি")
    st.image(image, use_container_width=True)

    st.markdown("---")
    
    # Image Enhancements
    contrast = st.slider("কন্ট্রাস্ট (Contrast) বাড়ান", 1.0, 3.0, 1.5)
    brightness = st.slider("ব্রাইটনেস (Brightness) বাড়ান", 1.0, 2.5, 1.2)

    enhancer1 = ImageEnhance.Contrast(image)
    img_enhanced = enhancer1.enhance(contrast)

    enhancer2 = ImageEnhance.Brightness(img_enhanced)
    final_img = enhancer2.enhance(brightness)

    st.subheader("🔍 প্রসেস করা স্পষ্ট ছবি")
    st.image(final_img, caption="ক্যাপচা বোঝার সুবিধার্থে ফিল্টার করা ছবি", use_container_width=True)
