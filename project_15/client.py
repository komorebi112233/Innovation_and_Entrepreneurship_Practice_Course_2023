import socket
import hashlib
import random

# 椭圆曲线参数
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2


# SM2 2P密钥协商
def sm2_2p():
    # 生成随机数k
    k = random.randint(1, n-1)

    # 生成公钥
    P = (Gx, Gy)
    Q1 = point_mult(k, P)
    Q2 = point_mult(k, P)

    # 发送公钥给服务器
    conn.sendall(bytes(str(Q1[0]), encoding="utf-8"))
    conn.sendall(bytes(str(Q1[1]), encoding="utf-8"))

    # 接收服务器的公钥
    Q2_x = int(conn.recv(1024).decode("utf-8"))
    Q2_y = int(conn.recv(1024).decode("utf-8"))
    Q2 = (Q2_x, Q2_y)

    # 计算共享密钥
    S1 = point_mult(k, Q2)
    S2 = point_mult(k, Q1)

    # 将共享密钥转换为字符串形式
    hex_S1 = hex(S1[0])[2:] + hex(S1[1])[2:]
    hex_S2 = hex(S2[0])[2:] + hex(S2[1])[2:]

    # 使用SHA256进行哈希
    hash_S1 = hashlib.sha256(bytes.fromhex(hex_S1)).digest()
    hash_S2 = hashlib.sha256(bytes.fromhex(hex_S2)).digest()

    # 输出共享密钥的哈希值
    print("Alice's shared key (hashed):", hash_S2.hex().upper())
    print("Bob's shared key (hashed):", hash_S1.hex().upper())

    return hash_S1, hash_S2


# 椭圆曲线点相加
def point_add(P, Q):
    if P == "O":
        return Q
    elif Q == "O":
        return P
    else:
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 != y2 or y1 == 0):
            return "O"
        else:
            if P != Q:
                lam = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
            else:
                lam = ((3 * x1**2 + a) * mod_inverse(2 * y1, p)) % p
            x3 = (lam**2 - x1 - x2) % p
            y3 = (lam * (x1 - x3) - y1) % p
            return x3, y3


# 椭圆曲线倍乘
def point_mult(k, P):
    binary = bin(k)[2:]
    Q = "O"
    for i in range(len(binary)):
        Q = point_add(Q, Q)
        if binary[i] == "1":
            Q = point_add(Q, P)
    return Q


# 求模逆
def mod_inverse(a, m):
    if a < 0 or m <= a:
        a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    if ud > 0:
        return ud
    else:
        return ud + m


# TCP客户端
def start_client():
    global conn
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 1000))
    print("Connected to server")
    data = s.recv(1024)
    print(data.decode("utf-8"))

    conn = s


if __name__ == "__main__":
    start_client()
    shared_key = sm2_2p()
