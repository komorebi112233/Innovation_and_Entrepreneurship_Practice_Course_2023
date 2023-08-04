import random

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = extended_gcd(b, a % b)
        return (d, y, x - (a // b) * y)

def ecmh_poc(n):
    # 选择一个随机的椭圆曲线参数
    a = random.randint(1, n-1)
    b = random.randint(1, n-1)
    
    # 选择一个随机的起始点
    x = random.randint(1, n-1)
    y = random.randint(1, n-1)
    
    # 计算初始斜率
    m = (3 * x**2 + a) * extended_gcd(2 * y, n)[1] % n
    
    # 开始ECMH算法
    while True:
        # 计算下一个点
        x = (m**2 - 2 * x) % n
        y = (m * (x - x) - y) % n
        
        # 计算最大公约数
        d = extended_gcd(2 * y, n)[0]
        
        if d != 1 and d != n:
            return d
        
        # 更新斜率
        m = (3 * x**2 + a) * extended_gcd(2 * y, n)[1] % n

# 测试
n = 123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899
factor = ecmh_poc(n)
print("n =", n)
print("Factor found:", factor)
