import streamlit as st
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

st.title("🔐 File Encryption & Decryption Tool")

password = st.text_input("Enter Password", type="password")

uploaded_file = st.file_uploader("Upload File")

if uploaded_file is not None and password:

    data = uploaded_file.read()
    key = generate_key(password)
    f = Fernet(key)

    if st.button("Encrypt File"):
        encrypted = f.encrypt(data)

        st.success("File encrypted successfully!")

        st.download_button(
            label="Download Encrypted File",
            data=encrypted,
            file_name="encrypted_file.enc"
        )

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
            st.error("Wrong password or invalid encrypted file")