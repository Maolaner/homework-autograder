
import streamlit as st
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import tempfile

# 标准答案字典
standard_answers = {
    "4-1": "to help",
    "4-2": "buying",
    "4-3": "to ask",
    "4-4": "being",
    "4-5": "showing",
    "4-6": "talking",
    "5-1": "to show",
    "5-2": "to indicate",
    "5-3": "going",
    "5-4": "to spend",
    "5-5": "to see",
    "5-6": "rising"
}

st.title("英语作业自动批改系统 📘")
uploaded_file = st.file_uploader("请上传学生作业（图片或PDF）", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    st.success("文件上传成功 ✅")

    # 提取文本
    ocr_text = ""
    if uploaded_file.name.lower().endswith(".pdf"):
        images = convert_from_bytes(uploaded_file.read(), 300)
        for img in images:
            ocr_text += pytesseract.image_to_string(img) + "\n"
    else:
        image = Image.open(uploaded_file)
        ocr_text = pytesseract.image_to_string(image)

    # 显示识别内容（可选）
    with st.expander("查看识别到的学生作业内容"):
        st.text(ocr_text)

    # 自动批改
    st.subheader("批改结果")
    student_text = ocr_text.lower()
    results = []
    for key, correct_answer in standard_answers.items():
        if correct_answer.lower() in student_text:
            results.append((key, correct_answer, correct_answer, "✔"))
        else:
            results.append((key, "未知", correct_answer, "✘"))

    # 展示表格
    import pandas as pd
    df = pd.DataFrame(results, columns=["题号", "学生答案", "正确答案", "判定"])
    st.table(df)
