import hashlib
import time

def sm3_hash(message):
    hash_obj = hashlib.new('sm3')
    hash_obj.update(message.encode('utf-8'))
    hex_hash_value = hash_obj.hexdigest()
    return hex_hash_value

def update_hash_with_iteration(message, iterations):
    hashed_message = message
    for i in range(iterations):
        hashed_message = sm3_hash(hashed_message)
    return hashed_message

# 示例用法
message = "Hello, world!"
num_iterations = 10  # 迭代次数
hashed_message = update_hash_with_iteration(message, num_iterations)
print(hashed_message)
