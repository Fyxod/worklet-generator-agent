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
            st.write(f"- {file.name} ({len(file.getvalue()) / 1024:.2f} KB)")

        if st.button("Generate worklets ->"):
            files_to_send = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]

            with st.spinner("Uploading files and generating worklets... ⏳"):
                try:
                    response = requests.post(FASTAPI_URL, files=files_to_send)
                    response.raise_for_status()  # Raises an error for HTTP failures
                    st.success("Files successfully uploaded! 🎉")
                    st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed: {e}")
