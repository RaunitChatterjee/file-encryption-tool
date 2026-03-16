# 🔐 File Encryption & Decryption Tool

A Python-based tool that securely encrypts and decrypts files using AES encryption.

## Features
- AES-based file encryption
- Password-protected security
- File decryption with correct password
- Command line interface
- Standalone executable using PyInstaller

## Technologies Used
- Python
- Cryptography library
- AES encryption
- PyInstaller

## Project Structure

file-encryption-tool
│
├── src
│   ├── encrypt.py
│   ├── decrypt.py
│   ├── generate_key.py
│   └── password_encryptor.py
│
├── examples
│   └── sample.txt
│
├── README.md
├── requirements.txt
└── .gitignore

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/file-encryption-tool.git

Install dependencies:

pip install -r requirements.txt

Run the tool:

python src/password_encryptor.py

## Example Usage

Choose option: 1  
Enter file to encrypt: sample.txt  
Enter password: mypassword

Encrypted output:

sample.txt.enc

## Author
Raunit Chatterjee