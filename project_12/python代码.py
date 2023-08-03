import hashlib
import ecdsa
from ecdsa.util import randrange_from_seed__trytryagain

# 生成ECDSA密钥对
def generate_ecdsa_key_pair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk

# 使用相同的随机数k进行ECDSA签名
def sign_ecdsa_with_same_k(sk, message):
    k = randrange_from_seed__trytryagain(sk.curve.generator.order(), sk.privkey.secret_multiplier)
    signature = sk.sign_deterministic(message, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der_canonize)
    return signature

# 生成Schnorr密钥对
def generate_schnorr_key_pair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk

# 使用相同的随机数k进行Schnorr签名
def sign_schnorr_with_same_k(sk, message):
    k = randrange_from_seed__trytryagain(sk.curve.generator.order(), sk.privkey.secret_multiplier)
    signature = sk.sign(message, k=k)
    return signature

# 生成SM2密钥对
def generate_sm2_key_pair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk

# 使用相同的随机数k进行SM2签名
def sign_sm2_with_same_k(sk, message):
    k = randrange_from_seed__trytryagain(sk.curve.generator.order(), sk.privkey.secret_multiplier)
    signature = sk.sign(message, k=k)
    return signature

# 验证ECDSA签名
def verify_ecdsa_signature(vk, message, signature):
    try:
        vk.verify(signature, message, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)
        return True
    except ecdsa.BadSignatureError:
        return False

# 验证Schnorr签名
def verify_schnorr_signature(vk, message, signature):
    try:
        vk.verify(signature, message)
        return True
    except ecdsa.BadSignatureError:
        return False

# 验证SM2签名
def verify_sm2_signature(vk, message, signature):
    try:
        vk.verify(signature, message)
        return True
    except ecdsa.BadSignatureError:
        return False

# 测试代码
def test():
    # 生成ECDSA密钥对
    ecdsa_sk, ecdsa_vk = generate_ecdsa_key_pair()

    # 使用相同的随机数k进行ECDSA签名
    message = b"Hello, world!"
    ecdsa_signature = sign_ecdsa_with_same_k(ecdsa_sk, message)

    # 验证ECDSA签名
    ecdsa_valid = verify_ecdsa_signature(ecdsa_vk, message, ecdsa_signature)
    print("ECDSA Signature Valid:", ecdsa_valid)

    # 生成Schnorr密钥对
    schnorr_sk, schnorr_vk = generate_schnorr_key_pair()

    # 使用相同的随机数k进行Schnorr签名
    schnorr_signature = sign_schnorr_with_same_k(schnorr_sk, message)

    # 验证Schnorr签名
    schnorr_valid = verify_schnorr_signature(schnorr_vk, message, schnorr_signature)
    print("Schnorr Signature Valid:", schnorr_valid)

    # 生成SM2密钥对
    sm2_sk, sm2_vk = generate_sm2_key_pair()

    # 使用相同的随机数k进行SM2签名
    sm2_signature = sign_sm2_with_same_k(sm2_sk, message)

    # 验证SM2签名
    sm2_valid = verify_sm2_signature(sm2_vk, message, sm2_signature)
    print("SM2 Signature Valid:", sm2_valid)

test()
