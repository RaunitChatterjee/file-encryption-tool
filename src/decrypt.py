from cryptography.fernet import Fernet

def load_key():
    return open("key.key", "rb").read()

def decrypt_file(filename):
    key = load_key()
    f = Fernet(key)

    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    new_name = filename.replace(".enc", "_decrypted.txt")

    with open(new_name, "wb") as file:
        file.write(decrypted_data)

    print("File decrypted successfully!")

file = input("Enter the file name to decrypt: ")
decrypt_file(file)