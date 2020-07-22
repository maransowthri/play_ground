from cryptography.fernet import Fernet

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def get_encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message

def get_decrypted_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()

if __name__ == "__main__":
    # encrypted_message = get_encrypt_message("JaiKrishna@1993")
    decrypted_message = get_decrypted_message(b'gAAAAABfGB6wN22gR76WRF3KBVn2EN4DFchpDgCSBpQyEvraGqHan3s3YJ479s45a_uvAY_QczYs_jhC9tCix3vDRIP7gCMJ_w==')
    # print(encrypted_message)
    print(decrypted_message)
