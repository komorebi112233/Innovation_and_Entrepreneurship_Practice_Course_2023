import struct
import hashlib
import time

def left_rotate(x, n):
    return ((x << (n % 32)) | (x >> (32 - (n % 32)))) & 0xFFFFFFFF


def sm3(message):
    message_len = len(message)
    append_bits_len = (448 - (message_len * 8 + 1)) % 512
    message += b'\x80'
    message += bytes(append_bits_len // 8)

    message += struct.pack('>Q', message_len * 8)

    IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
          0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]

    Tj = [0x79CC4519, 0x7A879D8A]
    W = [0] * 68
    W_prime = [0] * 64

    for i in range(0, len(message), 64):
        X = struct.unpack('>16I', message[i: i + 64])

        for j in range(16, 68):
            tmp = W[j - 16] ^ W[j - 9] ^ (left_rotate(W[j - 3], 15))
            W[j] = left_rotate(tmp, 1)

        for j in range(64):
            W_prime[j] = W[j] ^ W[j + 4]

        A, B, C, D, E, F, G, H = IV

        for j in range(64):
            if j < 16:
                SS1 = left_rotate(
                    left_rotate(A, 12) + E + left_rotate(Tj[0], j), 7)
                SS2 = SS1 ^ left_rotate(A, 12)
                TT1 = (FFj(A, B, C, j) + D + SS2 + W_prime[j]) & 0xFFFFFFFF
                TT2 = (GGj(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
                D = C
                C = left_rotate(B, 9)
                B = A
                A = TT1
                H = G
                G = left_rotate(F, 19)
                F = E
                E = P0(TT2)
            else:
                SS1 = left_rotate(
                    left_rotate(A, 12) + E + left_rotate(Tj[1], j - 16), 7)
                SS2 = SS1 ^ left_rotate(A, 12)
                TT1 = (FFj(A, B, C, j) + D + SS2 + W_prime[j]) & 0xFFFFFFFF
                TT2 = (GGj(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
                D = C
                C = left_rotate(B, 9)
                B = A
                A = TT1
                H = G
                G = left_rotate(F, 19)
                F = E
                E = P0(TT2)

        IV = [(IV[i] ^ A) & 0xFFFFFFFF for i in range(8)]

    return ''.join([format(x, '08x') for x in IV])

def FFj(X, Y, Z, j):
    if 0 <= j < 16:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)

def GGj(X, Y, Z, j):
    if 0 <= j < 16:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (~X & Z)

def P0(X):
    return X ^ left_rotate(X, 9) ^ left_rotate(X, 17)

# 测试例子
message = b'abcdefghijklmnopqrstuvwxyz'

start_time = time.time()
hash_value = sm3(message)
end_time = time.time()

print(hash_value)

execution_time = end_time - start_time
print("执行时间：", execution_time, "秒")



