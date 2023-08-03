from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

# 生成SM2密钥对
def generate_sm2_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# 使用SM2私钥签名消息
def sign_message(message, private_key):
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

# 使用SM2公钥验证签名
def verify_signature(message, signature, public_key):
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False

# 加密消息
def encrypt_message(message, public_key):
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public_key = ephemeral_private_key.public_key()

    shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'',
        backend=default_backend()
    ).derive(shared_key)

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ephemeral_public_key, iv, ciphertext

# 解密消息
def decrypt_message(ciphertext, iv, ephemeral_public_key, private_key):
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'',
        backend=default_backend()
    ).derive(shared_key)

    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    padded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return padded_data

# 保存SM2私钥到文件
def save_private_key(private_key, filename):
    pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as f:
        f.write(pem)

# 从文件加载SM2私钥
def load_private_key(filename):
    with open(filename, 'rb') as f:
        pem = f.read()
    private_key = serialization.load_pem_private_key(
        pem,
        password=None,
        backend=default_backend()
    )
    return private_key

# 保存SM2公钥到文件
def save_public_key(public_key, filename):
    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)

# 从文件加载SM2公钥
def load_public_key(filename):
    with open(filename, 'rb') as f:
        pem = f.read()
    public_key = serialization.load_pem_public_key(
        pem,
        backend=default_backend()
    )
    return public_key

# 示例用法
def example_usage():
    # 生成SM2密钥对
    private_key, public_key = generate_sm2_keypair()

    # 保存私钥和公钥到文件
    save_private_key(private_key, 'private_key.pem')
    save_public_key(public_key, 'public_key.pem')

    # 加载私钥和公钥
    private_key = load_private_key('private_key.pem')
    public_key = load_public_key('public_key.pem')

    # 要加密的消息
    message = b"Hello, World!"

    # 签名消息
    signature = sign_message(message, private_key)

    # 验证签名
    is_valid = verify_signature(message, signature, public_key)
    print("Signature is valid:", is_valid)

    # 加密消息
    ephemeral_public_key, iv, ciphertext = encrypt_message(message, public_key)

    # 解密消息
    decrypted_message = decrypt_message(ciphertext, iv, ephemeral_public_key, private_key)
    print("Decrypted message:", decrypted_message)

# 运行示例用法
example_usage()
