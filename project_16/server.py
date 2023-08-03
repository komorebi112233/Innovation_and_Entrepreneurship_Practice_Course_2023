import socket
from sm2 import SM2Cipher

def main():
    # 生成密钥对
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    cipher = SM2Cipher(p, a, b, n, X, Y)

    # 创建TCP socket并监听
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1000))
    server_socket.listen(1)
    print('等待客户端连接...')
    client_socket, client_address = server_socket.accept()
    print('客户端已连接:', client_address)

    # 接收加密数据并解密
    ciphertext = client_socket.recv(1024).strip()
    plaintext = cipher.decrypt(ciphertext)
    print('解密结果:', plaintext.decode())

    # 关闭连接
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()
