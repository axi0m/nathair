# Ref: https://www.thepythoncode.com/article/encrypt-decrypt-files-symmetric-python
# Ref2: https://cryptography.io/en/latest/fernet/

from cryptography.fernet import Fernet


def write_key():
    """
    Generates a key and saves it to a file
    """

    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Load key from current working directory
    """

    return open("key.key", "rb").read()


# Gen new key
write_key()

# Load key we created
key = load_key()

message = "some secret message".encode()

# init Fernet class
f = Fernet(key)

ciphertext = f.encrypt(message)

# print ciphertext
print(ciphertext)

# decrypted text
decrypted_text = f.decrypt(ciphertext)
print(decrypted_text)
