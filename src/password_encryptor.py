import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file():
    file_name = input("Enter file to encrypt: ")
    password = input("Enter password: ")

    key = generate_key(password)
    f = Fernet(key)

    with open(file_name, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    with open(file_name + ".enc", "wb") as file:
        file.write(encrypted)

    print("File encrypted successfully!")

def decrypt_file():
    file_name = input("Enter file to decrypt: ")
    password = input("Enter password: ")

    key = generate_key(password)
    f = Fernet(key)

    try:
        with open(file_name, "rb") as file:
            data = file.read()

        decrypted = f.decrypt(data)

        new_name = file_name.replace(".enc", "_decrypted")

        with open(new_name, "wb") as file:
            file.write(decrypted)

        print("File decrypted successfully!")

    except:
        print("Wrong password or corrupted file")

print("1. Encrypt File")
print("2. Decrypt File")

choice = input("Choose option: ")

if choice == "1":
    encrypt_file()

elif choice == "2":
    decrypt_file()

else:
    print("Invalid choice")