import hashlib
import random

def sm3_hash(message, salt):
    hash_obj = hashlib.new('sm3')
    # 在消息中添加盐值
    message_with_salt = message + str(salt)
    hash_obj.update(message_with_salt.encode('utf-8'))
    hex_hash_value = hash_obj.hexdigest()
    return hex_hash_value

# 示例用法
message = "Hello, world!"
salt = random.randint(1, 100)  # 生成一个随机的盐值
hashed_message = sm3_hash(message, salt)
print(hashed_message)
