import streamlit as st
import requests
import os
import urllib.parse  # For encoding file names

FASTAPI_URL = os.getenv("FASTAPI_URL", "https://api.katiyar.xyz")

st.set_option('server.maxUploadSize', 1000)  # in MB

st.set_page_config(page_title="Worklet Generator", layout="centered")
st.markdown(
    """
    <style>
    a {
        color: white !important;
        text-decoration: none !important;
    }
    a:hover {
        color: lightgray !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Upload up to 5 worklets")

# Model selection
model_options = [
    "gemini-flash-2.0",
    "deepseek-r1:70b",
    "llama3.3:latest",
    "gemma3:27b"
]
selected_model = st.selectbox("Choose a model to use", model_options)

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
                    # Include model as a query parameter
                    model_param = urllib.parse.quote(selected_model)
                    response = requests.post(f"{FASTAPI_URL}/upload?model={model_param}", files=files_to_send)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if "files" in data:
                        st.success("Files successfully generated! 🎉")
                        st.write("### Download Generated PDFs:")
                        for file in data["files"]:
                            file_name_encoded = urllib.parse.quote(file["name"])
                            download_url = f"{FASTAPI_URL}/download/{file_name_encoded}"
                            st.markdown(f"[📄 {file['name']}]({download_url})")

                        zip_download_url = f"{FASTAPI_URL}/download_all"
                        st.markdown(f"### 📥 [Download All as ZIP]({zip_download_url})")
                    else:
                        st.error("Unexpected response format.")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed: {e}")
