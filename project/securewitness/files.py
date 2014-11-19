import uuid

from Crypto.Cipher import AES

def encrypt(src, dst, key):
    iv = uuid.uuid4()
    dst.write(iv.bytes)
    crypto = AES.new(key.bytes, AES.MODE_CFB, iv.bytes)
    for chunk in src.chunks():
        dst.write(crypto.encrypt(chunk))


def decrypt(file, key):
    pass
