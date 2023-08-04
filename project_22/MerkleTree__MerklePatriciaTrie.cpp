#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

// Merkle Tree节点的结构定义
struct MerkleTreeNode {
    std::string data;
    std::string hash;
};

// Merkle Patricia Trie节点的结构定义
struct MPTNode {
    std::string key;
    std::string value;
    std::unordered_map<std::string, MPTNode*> children;
};

// 计算哈希值的函数，这里使用简单的字符串拼接来代替实际的哈希计算操作
std::string calculateHash(const std::string& data) {
    return data;  // 简化，返回数据本身作为哈希值
}

// 将Merkle Tree转换为Merkle Patricia Trie的函数
MPTNode* convertToMPT(const std::vector<MerkleTreeNode>& merkleTree) {
    MPTNode* root = new MPTNode();
    root->key = "Root_MPT";

    for (const auto& node : merkleTree) {
        MPTNode* mptNode = new MPTNode();
        mptNode->key = calculateHash(node.data);
        mptNode->value = node.data;

        root->children[mptNode->key] = mptNode;
    }

    return root;
}

// 打印Merkle Patricia Trie的函数，用于检查转换结果
void printMPT(MPTNode* node, int depth = 0) {
    if (!node) {
        return;
    }

    std::string indent(depth * 4, ' ');
    std::cout << indent << "Key: " << node->key << ", Value: " << node->value << std::endl;

    for (const auto& child : node->children) {
        printMPT(child.second, depth + 1);
    }
}

int main() {
    // 构建一个简单的Merkle Tree
    std::vector<MerkleTreeNode> merkleTree = {
        {"A", ""},
        {"B", ""},
        {"C", ""},
        {"D", ""}
    };

    // 计算Merkle Tree中节点的哈希值
    for (auto& node : merkleTree) {
        node.hash = calculateHash(node.data);
    }

    // 将Merkle Tree转换为Merkle Patricia Trie
    MPTNode* rootMPT = convertToMPT(merkleTree);

    // 打印Merkle Patricia Trie，用于检查转换结果
    printMPT(rootMPT);

    // TODO: 释放内存，避免内存泄漏

    return 0;
}
