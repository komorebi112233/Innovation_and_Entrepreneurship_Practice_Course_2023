import hashlib

def sm3_hash(message, output_length):
    hash_obj = hashlib.new('sm3')
    hash_obj.update(message.encode('utf-8'))
    # 获取原始的哈希值
    hash_value = hash_obj.digest()

    # 转换为十六进制字符串
    hex_hash_value = hash_obj.hexdigest()

    # 将哈希值截取到指定长度
    truncated_hash = hex_hash_value[:output_length]

    return truncated_hash

# 示例用法
message = "Hello, world!"
output_length = 64  # 增加输出长度到64个字符（256位）
hashed_message = sm3_hash(message, output_length)
print(hashed_message)
