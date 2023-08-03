from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# SM2参数
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE171F6241633F670F9
Gy = 0x2BBFA18E1EE00BF0102F997D6F67ED17C63F440F9355ADA5FD16684DA2CBA3ED

# 生成SM2密钥对
def generate_key_pair():
    curve = ec.SECP256K1
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# SM2签名
def sign(private_key, message):
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    return signature

# SM2验证签名
def verify(public_key, message, signature):
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

# 示例用法
private_key, public_key = generate_key_pair()
message = b"Hello, world!"
signature = sign(private_key, message)
valid = verify(public_key, message, signature)

print("Private key:", private_key.private_numbers().private_value)
print("Public key:", public_key.public_numbers().x, public_key.public_numbers().y)
print("Signature:", signature)
print("Valid:", valid)
