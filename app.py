Import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Streamlit Page Config
st.set_page_config(
    page_title="CAPTCHA Solver Helper",
    page_icon="🧩",
    layout="centered"
)

st.title("🧩 CAPTCHA Solver Helper")
st.write("ক্যাপচা ইমেজ আপলোড করুন এবং প্রি-প্রসেসিং প্রয়োগ করে টেক্সট বের করুন।")

# Tesseract Path Configuration (Windows এর জন্য প্রয়োজন হলে নিচের লাইনটি আনকমেন্ট করুন)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# File Uploader
uploaded_file = st.file_uploader("একটি CAPTCHA ইমেজ ফাইল বেছে নিন (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

def preprocess_image(image, threshold_val, blur_kernel):
    """
    ইমেজ ফিল্টারিং ও নয়েজ দূর করার জন্য প্রি-প্রসেসিং ফাংশন
    """
    # PIL Image to OpenCV format
    img_np = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # Gaussian Blur (নয়েজ কমানোর জন্য)
    if blur_kernel > 0:
        if blur_kernel % 2 == 0:
            blur_kernel += 1  # Kernel size must be odd
        gray = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        
    # Thresholding (বাইনারি ইমেজে রূপান্তর)
    _, thresh = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY)
    
    return gray, thresh

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("মূল ইমেজ")
        st.image(original_image, use_container_width=True)
        
    # Pre-processing Controls
    st.sidebar.header("প্রি-প্রসেসিং সেটিংস")
    threshold = st.sidebar.slider("Threshold Value", 0, 255, 127)
    blur_val = st.sidebar.slider("Blur Intensity", 0, 9, 1)
    
    # Preprocess execution
    gray_img, processed_img = preprocess_image(original_image, threshold, blur_val)
    
    with col2:
        st.subheader("প্রসেস করা ইমেজ")
        st.image(processed_img, use_container_width=True)
        
    st.markdown("---")
    
    # Solve Action
    if st.button("ক্যাপচা সলভ করুন", type="primary"):
        with st.spinner("OCR প্রসেসিং চলছে..."):
            try:
                # Custom OCR configuration for alphanumeric CAPTCHAs
                custom_config = r'--oem 3 --psm 6'
                extracted_text = pytesseract.image_to_string(processed_img, config=custom_config).strip()
                
                if extracted_text:
                    st.success(f"**সনাক্তকৃত ক্যাপচা কোড:** `{extracted_text}`")
                    st.code(extracted_text, language="text")
                else:
                    st.warning("কোনো টেক্সট পাওয়া যায়নি। সাইডবারের Threshold বা Blur সেটিংস অ্যাডজাস্ট করে আবার চেষ্টা করুন।")
            except Exception as e:
                st.error(f"OCR প্রসেস করতে সমস্যা হয়েছে: {e}")
                st.info("আপনার পিসিতে Tesseract-OCR ইনস্টল করা আছে কিনা নিশ্চিত করুন।")
else:
    st.info("শুরু করতে একটি CAPTCHA ইমেজ ফাইল আপলোড করুন।")