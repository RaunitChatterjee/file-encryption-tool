import streamlit as st
import base64
import hashlib
from cryptography.fernet import Fernet

st.set_page_config(page_title="File Encryption Tool", page_icon="🔐")

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

st.title("🔐 File Encryption & Decryption Tool")
st.write("Secure your files using password-based AES encryption.")

password = st.text_input("Enter Password", type="password")

uploaded_file = st.file_uploader("Upload File")

col1, col2 = st.columns(2)

if uploaded_file and password:

    data = uploaded_file.read()
    key = generate_key(password)
    f = Fernet(key)

    with col1:
        if st.button("Encrypt File"):
            encrypted = f.encrypt(data)

            st.success("File encrypted successfully!")

            st.download_button(
                label="Download Encrypted File",
                data=encrypted,
                file_name="encrypted_file.enc"
            )

    with col2:
        if st.button("Decrypt File"):
            try:
                decrypted = f.decrypt(data)

                st.success("File decrypted successfully!")

                st.download_button(
                    label="Download Decrypted File",
                    data=decrypted,
                    file_name="decrypted_file.txt"
                )

            except:
                st.error("Wrong password or invalid file")

st.markdown("---")
st.caption("Built by Raunit Chatterji • Python Encryption Tool")