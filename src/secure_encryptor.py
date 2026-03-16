import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    key = generate_key(password)
    f = Fernet(key)

    with open(file_path, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted)

    messagebox.showinfo("Success", "File encrypted")

def decrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    key = generate_key(password)
    f = Fernet(key)

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        decrypted = f.decrypt(data)

        new_name = file_path.replace(".enc", "_decrypted")

        with open(new_name, "wb") as file:
            file.write(decrypted)

        messagebox.showinfo("Success", "File decrypted")

    except:
        messagebox.showerror("Error", "Wrong password or file")

root = tk.Tk()
root.title("File Encryption Tool")
root.geometry("400x200")

tk.Label(root, text="Enter Password").pack(pady=10)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack()

tk.Button(root, text="Encrypt File", command=encrypt_file).pack(pady=10)
tk.Button(root, text="Decrypt File", command=decrypt_file).pack(pady=10)

root.mainloop()