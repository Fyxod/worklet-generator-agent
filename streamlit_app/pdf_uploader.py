import streamlit as st
import requests
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/upload")

st.set_page_config(page_title="Worklet Generator", layout="centered")

st.title("Upload up to 5 worklets")

uploaded_files = st.file_uploader("Choose up to 5 PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("You can only upload up to 5 PDF files.")
    else:
        st.success(f"You have uploaded {len(uploaded_files)} file(s).")
        st.write("### Uploaded Files:")
        for file in uploaded_files:
            st.write(f"- {file.name}")
        
        if st.button("Generate worklets ->"):
            files_to_send = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]
            response = requests.post(FASTAPI_URL, files=files_to_send)
            
            if response.status_code == 200:
                st.success("Files successfully uploaded!")
                st.json(response.json())
            else:
                st.error("Failed to upload files. Please try again.")
