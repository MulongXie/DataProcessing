from Grammar_Tree import Tree
import json

data = json.load(open('27.json'))
tree = Tree(data['annotations'])

print(tree.token_map)
for i in range(len(tree.subtrees)):
    print(tree.subtrees[i])
    print(tree.subtrees_encoded[i])