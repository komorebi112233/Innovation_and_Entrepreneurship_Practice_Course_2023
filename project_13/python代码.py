from hashlib import sha256
from ecpy.curves import Curve, Point

# 选择椭圆曲线
curve = Curve.get_curve('secp256k1')

# 哈希函数
def hash_element(element):
    return curve.generator * int(sha256(str(element).encode()).hexdigest(), 16)

# 点加法操作
def add_points(point1, point2):
    return point1 + point2

# 构建空集映射
empty_set_mapping = curve.infinity

# 计算多重集的摘要
def compute_digest(multiset):
    digest = empty_set_mapping
    for element in multiset:
        element_hash = hash_element(element)
        digest = add_points(digest, element_hash)
    return digest

# 示例用法
multiset1 = [1, 2, 3]
multiset2 = [2, 3, 4]

digest1 = compute_digest(multiset1)
digest2 = compute_digest(multiset2)

print("Digest 1:", digest1)
print("Digest 2:", digest2)

