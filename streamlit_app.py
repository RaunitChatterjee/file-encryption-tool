import streamlit as st
import base64
import hashlib
from cryptography.fernet import Fernet

# Page configuration
st.set_page_config(
    page_title="File Encryption Tool",
    page_icon="🔐",
    layout="centered"
)

# Function to generate encryption key
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# Title and description
st.title("🔐 File Encryption & Decryption Tool")
st.write("Secure your files using password-based AES encryption.")

st.divider()

# Upload file
uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:

    st.subheader("Choose Operation")

    action = st.radio(
        "Select action",
        ("Encrypt File", "Decrypt File")
    )

    password = st.text_input("Enter Password", type="password")

    if password:

        data = uploaded_file.read()
        key = generate_key(password)
        f = Fernet(key)

        if st.button("Process File"):

            with st.spinner("Processing file..."):

                if action == "Encrypt File":

                    encrypted = f.encrypt(data)

                    st.success("File encrypted successfully!")

                    st.download_button(
                        label="Download Encrypted File",
                        data=encrypted,
                        file_name="encrypted_file.enc"
                    )

                else:

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

st.divider()

# Reset button
if st.button("Reset Tool"):
    st.rerun()

st.caption("Built by Raunit Chatterjee • Python Encryption Tool")