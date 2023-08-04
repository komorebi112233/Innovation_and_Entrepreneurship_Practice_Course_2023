#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

// Merkle Tree�ڵ�Ľṹ����
struct MerkleTreeNode {
    std::string data;
    std::string hash;
};

// Merkle Patricia Trie�ڵ�Ľṹ����
struct MPTNode {
    std::string key;
    std::string value;
    std::unordered_map<std::string, MPTNode*> children;
};

// �����ϣֵ�ĺ���������ʹ�ü򵥵��ַ���ƴ��������ʵ�ʵĹ�ϣ�������
std::string calculateHash(const std::string& data) {
    return data;  // �򻯣��������ݱ�����Ϊ��ϣֵ
}

// ��Merkle Treeת��ΪMerkle Patricia Trie�ĺ���
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

// ��ӡMerkle Patricia Trie�ĺ��������ڼ��ת�����
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
    // ����һ���򵥵�Merkle Tree
    std::vector<MerkleTreeNode> merkleTree = {
        {"A", ""},
        {"B", ""},
        {"C", ""},
        {"D", ""}
    };

    // ����Merkle Tree�нڵ�Ĺ�ϣֵ
    for (auto& node : merkleTree) {
        node.hash = calculateHash(node.data);
    }

    // ��Merkle Treeת��ΪMerkle Patricia Trie
    MPTNode* rootMPT = convertToMPT(merkleTree);

    // ��ӡMerkle Patricia Trie�����ڼ��ת�����
    printMPT(rootMPT);

    // TODO: �ͷ��ڴ棬�����ڴ�й©

    return 0;
}
