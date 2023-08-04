import hashlib
import time

def construct_merkle_tree(leaves):
    if len(leaves) == 1:
        return leaves[0]
    
    next_level = []
    for i in range(0, len(leaves), 2):
        leaf1 = leaves[i]
        leaf2 = leaves[i+1] if i+1 < len(leaves) else leaf1
        combined = leaf1 + leaf2
        hash_value = hashlib.sha256(combined.encode()).hexdigest()
        next_level.append(hash_value)
    
    return construct_merkle_tree(next_level)

def get_inclusion_proof(merkle_tree, leaf_index):
    proof = []
    current_index = leaf_index
    for level in merkle_tree:
        if current_index % 2 == 1:
            sibling_index = current_index - 1
        else:
            sibling_index = current_index + 1
        
        proof.append(merkle_tree[sibling_index])
        current_index //= 2
    
    return proof

def get_exclusion_proof(merkle_tree, leaf_index):
    proof = []
    current_index = leaf_index
    for level in merkle_tree:
        proof.append(level[current_index])
        current_index //= 2
    
    return proof


# 构造叶子节点
start_time = time.time()
leaves = [hashlib.sha256(str(i).encode()).hexdigest() for i in range(10**5)]
end_time = time.time()
execution_time = end_time - start_time
print("构造叶子节点_执行时间：", execution_time, "秒")


# 构造Merkle树
start_time1 = time.time()
merkle_tree = [leaves]
while len(merkle_tree[-1]) > 1:
    merkle_tree.append(construct_merkle_tree(merkle_tree[-1]))
end_time1 = time.time()
execution_time1 = end_time1 - start_time1
print("构造Merkle树_执行时间：", execution_time1, "秒")


# 选择一个特定的叶子节点
start_time2 = time.time()
leaf_index = 42
selected_leaf = leaves[leaf_index]
end_time2 = time.time()
execution_time2 = end_time2 - start_time2
print("选择一个特定的叶子节点_执行时间：", execution_time2, "秒")

# 生成包含证明
start_time3 = time.time()
inclusion_proof = get_inclusion_proof(merkle_tree, leaf_index)
end_time3 = time.time()
execution_time3 = end_time3 - start_time3
print("生成包含证明_执行时间：", execution_time3, "秒")

# 生成排除证明
start_time4 = time.time()
exclusion_proof = get_exclusion_proof(merkle_tree, leaf_index)
end_time4 = time.time()
execution_time4 = end_time4 - start_time4
print("生成包含证明_执行时间：", execution_time4, "秒")

print("Selected Leaf:", selected_leaf)
print("Inclusion Proof:", inclusion_proof)
print("Exclusion Proof:", exclusion_proof)
