import hashlib
import time

# 受信任的发行机构
def trusted_issuer():
    seed = b'random_seed'  # 128位随机种子，可以根据实际情况修改
    hashed_seed = hashlib.sha256(seed).digest()  # 计算种子的哈希值
    return hashed_seed

# Alice证明她的年龄大于等于21岁给Bob
def prove_age_to_bob(birth_year):
    current_year = 2021  # 当前年份，可以根据实际情况修改
    age_diff = current_year - birth_year

    # 计算证明信息
    hashed_seed = trusted_issuer()
    proof = hashlib.sha256(bytes([age_diff]) + hashed_seed).digest()

    return proof

# Bob验证Alice的证明
def verify_proof(proof):
    remaining_years = 2100 - 2021  # 剩余年份，可以根据实际情况修改

    # 计算待验证的证明信息
    hashed_seed = trusted_issuer()
    proof_to_verify = hashlib.sha256(bytes([remaining_years]) + proof).digest()

    # 检查证明信息是否有效
    if proof_to_verify == proof:
        return True
    else:
        return False

# 测试示例
alice_birth_year = 1990  # Alice的出生年份，可以根据实际情况修改

proof = prove_age_to_bob(alice_birth_year)

start_time = time.time()
verification_result = verify_proof(proof)
end_time = time.time()
execution_time = end_time - start_time
print("执行时间：", execution_time, "秒")

print("Verification Result:", verification_result)
