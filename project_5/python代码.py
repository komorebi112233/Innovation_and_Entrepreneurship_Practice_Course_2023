import hashlib

class MerkleTree:
    def __init__(self, data):
        self.data = data
        self.tree = []
        self.build_tree()

    def build_tree(self):
        # 构建叶节点
        for d in self.data:
            leaf_hash = hashlib.sha256(d.encode()).hexdigest()
            self.tree.append(leaf_hash)

        # 构建非叶节点
        level = self.tree[:]
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                node_hash = hashlib.sha256((level[i] + level[i+1]).encode()).hexdigest()
                next_level.append(node_hash)
            level = next_level[:]

        self.tree = level # 根节点

    def get_root(self):
        return self.tree[0]

# 测试代码
data = ["Hello", "World"]
merkle_tree = MerkleTree(data)
print("根节点哈希值:", merkle_tree.get_root())
