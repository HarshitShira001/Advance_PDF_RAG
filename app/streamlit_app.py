import streamlit as st
import requests

# Backend base URL
BASE_URL = "http://localhost:8000"  # Update this if deployed

st.set_page_config(page_title="📄 PDF Q&A System", layout="centered")
st.title("📄 Ask a Question on Your PDF")

# 1. Upload Section
st.header("Upload PDF and Ask a Question")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
question = st.text_input("Enter your question")

if st.button("Upload and Ask"):
    if not uploaded_file or not question:
        st.warning("Please upload a PDF and enter a question.")
    else:
        with st.spinner("Uploading and processing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                data = {"question": question}

                response = requests.post(f"{BASE_URL}/upload", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    st.write("BACKEND RESPONSE:", result)
                    file_id = result.get("file_id")
                    pdf_url = result.get("pdf_url")
                    st.success(f"Uploaded successfully! File ID: `{file_id}`")

                    st.session_state["file_id"] = file_id  
                    st.session_state["pdf_url"] = pdf_url
                    # Store for use below
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state.get("pdf_url"):
    st.link_button(
        "View PDF",
        st.session_state["pdf_url"]
    )
    
st.divider()

# 2. Status & Result Section
st.header("🔍 Check File Processing Status")

file_id_input = st.text_input("Enter File ID to Check Status", value=st.session_state.get("file_id", ""))

if st.button("Check Status"):
    if not file_id_input:
        st.warning("Please enter a file ID.")
    else:
        with st.spinner("Fetching status..."):
            try:
                response = requests.get(f"{BASE_URL}/{file_id_input}")
                if response.status_code == 200:
                    data = response.json()

                    st.info(f"📄 File Name: {data['name']}")
                    st.write(f"🟡 Status: `{data['status']}`")

                    if data.get("result"):
                        st.success("✅ Result:")
                        st.write(data["result"])
                    else:
                        st.warning("Result not ready yet. Please check back later.")

                else:
                    st.error("File not found or error fetching data.")
            except Exception as e:
                st.error(f"Error: {e}")
