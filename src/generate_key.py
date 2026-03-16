from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()

# Save key to file
with open("key.key", "wb") as file:
    file.write(key)

print("Key generated successfully")