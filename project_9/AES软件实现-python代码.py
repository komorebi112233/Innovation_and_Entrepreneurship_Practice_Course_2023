from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 密钥，注意密钥长度需要与所选AES模式相对应
key = get_random_bytes(32)  # 256位密钥

# 原始明文
plaintext = b'This is the plaintext message.'

# 执行填充操作
padded_plaintext = pad(plaintext, AES.block_size)

# 创建AES加密器
cipher = AES.new(key, AES.MODE_ECB)

# 加密数据
ciphertext = cipher.encrypt(padded_plaintext)

# 解密数据（可选）
decipher = AES.new(key, AES.MODE_ECB)
decrypted_data = decipher.decrypt(ciphertext)
unpadded_decrypted_data = unpad(decrypted_data, AES.block_size)

# 输出结果
print("密文:", ciphertext)
print("解密后的明文:", unpadded_decrypted_data.decode())
