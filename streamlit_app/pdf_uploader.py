import streamlit as st
import requests
import os
import urllib.parse
import mimetypes

FASTAPI_URL = os.getenv("FASTAPI_URL", "https://api.katiyar.xyz")

st.set_page_config(page_title="Worklet Generator", layout="centered")
st.markdown("""
<style>
a {
    color: white !important;
    text-decoration: none !important;
}
a:hover {
    color: lightgray !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Upload up to 5 worklets")

# Session state
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "response_data" not in st.session_state:
    st.session_state.response_data = None
if "link_list" not in st.session_state:
    st.session_state.link_list = [""]  # Start with one empty field

# Model selector
model_display_map = {
    "Gemini Flash 2.0": "gemini-flash-2.0",
    "DeepSeek R1 (70B)": "deepseek-r1:70b",
    "LLaMA 3.3": "llama3.3:latest",
    "Gemma 3 (27B)": "gemma3:27b",
    "Command A": "command-a:latest"
}
selected_display_name = st.selectbox("Choose a model to use", list(model_display_map.keys()))
selected_model = model_display_map[selected_display_name]

# Clear button
if st.button("🗑️ Clear uploaded files"):
    st.session_state.uploader_key += 1
    st.session_state.uploaded = False
    st.session_state.response_data = None
    st.rerun()

# File uploader
allowed_types = ["pdf", "pptx", "docx"]
uploaded_files = st.file_uploader(
    "Choose up to 5 PDF, PPTX, or DOCX files",
    type=allowed_types,
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

# Links input section
st.markdown("### Add any number of links")
link_count = len(st.session_state.link_list)
for i in range(link_count):
    st.session_state.link_list[i] = st.text_input(f"Link {i+1}", value=st.session_state.link_list[i], key=f"link_{i}")

if st.button("➕ Add another link"):
    st.session_state.link_list.append("")

if uploaded_files:
    if len(uploaded_files) > 5:
        st.error("You can only upload up to 5 files.")
    else:
        st.success(f"You have uploaded {len(uploaded_files)} file(s).")
        st.write("### Uploaded Files:")
        for file in uploaded_files:
            st.write(f"- {file.name} ({len(file.getvalue()) / 1024:.2f} KB)")

        if st.button("Generate worklets ->"):
            files_to_send = []
            for file in uploaded_files:
                mime_type, _ = mimetypes.guess_type(file.name)
                mime_type = mime_type or "application/octet-stream"
                files_to_send.append(("files", (file.name, file.getvalue(), mime_type)))

            # Filter out empty strings
            valid_links = [link for link in st.session_state.link_list if link.strip()]
            json_payload = {"links": valid_links}
            model_param = urllib.parse.quote(selected_model)

            with st.spinner("Uploading files and generating worklets... ⏳"):
                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/upload?model={model_param}",
                        files=files_to_send,
                        data={"links": str(valid_links)}  # You can also use `json=json_payload` if the backend expects JSON
                    )
                    response.raise_for_status()
                    st.session_state.response_data = response.json()
                    st.session_state.uploaded = True
                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed: {e}")
                    st.session_state.uploaded = False
                    st.session_state.response_data = None

# Results
if st.session_state.uploaded and st.session_state.response_data:
    data = st.session_state.response_data

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
