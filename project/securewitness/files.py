import uuid

from Crypto.Cipher import AES

def file_buffer(f, size=1024):
    while True:
        chunk = f.read(size)
        if not chunk: break
        yield chunk


def encrypt(src, dst, key):
    '''
    Encrypts src and stores it in dst using key
    src: file open for reading
    dst: file open for writing
    key: uuid
    '''
    iv = uuid.uuid4()
    dst.write(iv.bytes)
    crypto = AES.new(key.bytes, AES.MODE_CFB, iv.bytes)
    for chunk in file_buffer(src):
        dst.write(crypto.encrypt(chunk))


def decrypt(src, dst, key):
    '''
    Decrypts src and stores it in dst using key
    src: encrypted file open for reading
    dst: file open for writing
    key: uuid
    '''    
    crypto = AES.new(key.bytes, AES.MODE_CFB, src.read(16))
    for chunk in file_buffer(src):
        dst.write(crypto.decrypt(chunk))
