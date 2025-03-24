import streamlit as st
import requests
import os
import zipfile
import io
import urllib.parse  # Import URL encoding module


FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(page_title="Worklet Generator", layout="centered")
st.markdown(
    """
    <style>
    a {
        color: white !important;  /* Change link color to white */
        text-decoration: none !important;  /* Remove underline */
    }
    a:hover {
        color: lightgray !important;  /* Change hover color */
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
                    response = requests.post(f"{FASTAPI_URL}/upload", files=files_to_send)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if "files" in data:
                        st.success("Files successfully generated! 🎉")

                        # Display download links with proper URL encoding
                        st.write("### Download Generated PDFs:")
                        for file in data["files"]:
                            file_name_encoded = urllib.parse.quote(file["name"])  # Encode filename for URL
                            download_url = f"{FASTAPI_URL}/download/{file_name_encoded}"
                            st.markdown(f"[📄 {file['name']}]({download_url})")

                    else:
                        st.error("Unexpected response format.")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed: {e}")
