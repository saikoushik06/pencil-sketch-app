import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

def pencil_sketch(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blurred = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
    return sketch

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
            text-align: center;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🖼️ Pencil Sketch Converter")
st.markdown("Convert your images into realistic pencil sketches easily! 🖌️")

uploaded_file = st.file_uploader("📷 Upload an image to convert:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    sketch = pencil_sketch(image_np)
    
    st.image(image, caption='🖼️ Original Image', use_column_width=True)
    st.image(sketch, caption='✏️ Pencil Sketch', use_column_width=True, channels="GRAY")
    
    buf = io.BytesIO()
    sketch_pil = Image.fromarray(sketch)
    sketch_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(label="⬇️ Download Sketch", data=byte_im, file_name="pencil_sketch.png", mime="image/png")
