import os
from typing import Optional
import rsa
from rsa.pkcs1 import DecryptionError

PUBLIC_KEY_PATH = os.environ["NEED_PROJECT_PUBLIC_KEY"]
PRIVATE_KEY_PATH = os.environ["NEED_PROJECT_PRIVATE_KEY"]


def encrypt_message(message: bytes) -> bytes:
    with open(PUBLIC_KEY_PATH, "rb") as pub_f:
        pub_key = rsa.PublicKey.load_pkcs1(pub_f.read())

    encrypted_message = rsa.encrypt(message, pub_key=pub_key)
    return encrypted_message


def decrypt_message(message: bytes) -> Optional[bytes]:
    with open(PRIVATE_KEY_PATH, "rb") as priv_f:
        priv_key = rsa.PrivateKey.load_pkcs1(priv_f.read())

    try:
        decrypted_message = rsa.decrypt(message, priv_key=priv_key)
        return decrypted_message
    except DecryptionError:
        return None
