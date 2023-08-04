import hashlib

# 定义旋转操作函数
def rotate_left(x, n):
    return (x << n) | (x >> (32 - n))

# 定义压缩函数
def compress(block, h):
    w = [0] * 68

    # 消息扩展
    for i in range(16):
        w[i] = int.from_bytes(block[i * 4:(i + 1) * 4], 'big')
    for i in range(16, 68):
        w[i] = rotate_left(w[i - 16] ^ w[i - 9] ^ (rotate_left(w[i - 3], 15)), 1) ^ rotate_left(w[i - 13], 7) ^ w[i - 6]

    # 压缩
    a, b, c, d, e, f, g, _h = h
    for i in range(64):
        ss1 = rotate_left((rotate_left(a, 12) + e + rotate_left(0x79CC4519, i % 32)) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ rotate_left(a, 12)
        tt1 = ((a + ss1 + ((e & f) ^ (~e & g)) + 0x7A879D8A + w[i]) & 0xFFFFFFFF)
        tt2 = (ss2 + ((a & b) ^ (a & c) ^ (b & c))) & 0xFFFFFFFF
        a, b, c, d, e, f, g, _h = (_h, a, rotate_left(b, 9), c, d, e, f, tt1)

    # 更新哈希值
    h[0] = (h[0] + a) & 0xFFFFFFFF
    h[1] = (h[1] + b) & 0xFFFFFFFF
    h[2] = (h[2] + c) & 0xFFFFFFFF
    h[3] = (h[3] + d) & 0xFFFFFFFF
    h[4] = (h[4] + e) & 0xFFFFFFFF
    h[5] = (h[5] + f) & 0xFFFFFFFF
    h[6] = (h[6] + g) & 0xFFFFFFFF
    h[7] = (h[7] + _h) & 0xFFFFFFFF

    return [_h]

# 定义SM3哈希函数
def sm3(data):
    h = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]  # 初始哈希值
    length = len(data)
    count = length // 64 + 1 if length % 64 >= 56 else length // 64  # 消息分组数量

    for i in range(count - 1):
        block = data[i * 64:(i + 1) * 64]
        h = compress(block, h)

    last_block = bytearray()
    last_block.extend(data[(count - 1) * 64:])
    last_block.append(0x80)

    if len(last_block) > 56:
        h = compress(last_block, h)
        last_block = bytearray()

    last_block += bytearray(56 - len(last_block))
    last_block.extend(length.to_bytes(8, 'big'))

    h = compress(last_block, h)

    digest = b''
    for x in h:
        digest += x.to_bytes(4, 'big')

    return digest

# 测试代码
message = b'This is a test message'
hash_value = sm3(message)
print(hashlib.new('sm3', message).hexdigest())  # 原始SM3算法的结果
print(hash_value.hex())  # 简化SM3算法的结果
