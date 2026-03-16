from cryptography.fernet import Fernet

def load_key():
    return open("key.key", "rb").read()

def encrypt_file(filename):
    key = load_key()
    f = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)

    print("File encrypted successfully!")

file = input("Enter the file name to encrypt: ")
encrypt_file(file)