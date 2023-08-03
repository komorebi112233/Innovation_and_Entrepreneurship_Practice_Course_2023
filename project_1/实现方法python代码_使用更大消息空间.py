import hashlib
import random
import string

def generate_random_message(message_length):
    characters = string.ascii_letters + string.digits
    message = ''.join(random.choice(characters) for _ in range(message_length))
    return message

def sm3_hash(message):
    hash_obj = hashlib.new('sm3')
    hash_obj.update(message.encode('utf-8'))
    hex_hash_value = hash_obj.hexdigest()
    return hex_hash_value

# 示例用法
message_length = 1000  # 增加消息长度到1000个字符
message = generate_random_message(message_length)
hashed_message = sm3_hash(message)
print(hashed_message)
