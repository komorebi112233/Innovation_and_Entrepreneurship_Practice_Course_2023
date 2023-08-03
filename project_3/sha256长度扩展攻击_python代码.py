import hashlib

def sha256_length_extension_attack(original_hash, original_message, appended_data):
    # 获取原始哈希值的状态
    h = [int(original_hash[i:i+8], 16) for i in range(0, len(original_hash), 8)]

    # 获取原始消息的长度
    original_length = len(original_message)

    # 计算填充位数
    padding = b'\x80' + b'\x00' * ((55 - original_length) % 64) + original_length.to_bytes(8, 'big')

    # 构造附加数据的伪造消息
    forged_message = original_message + padding + appended_data

    # 计算伪造消息的哈希值
    h2 = hashlib.sha256(appended_data).digest()

    # 构造伪造消息的哈希值
    forged_hash = ''.join([format(h2[i], '02x') for i in range(len(h2))])

    return forged_message, forged_hash

# 示例使用
original_hash = '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069'
original_message = b'My secret message'
appended_data = b'Additional data'

forged_message, forged_hash = sha256_length_extension_attack(original_hash, original_message, appended_data)

print("Original Message: ", original_message)
print("Forged Message: ", forged_message)
print("Forged Hash: ", forged_hash)
