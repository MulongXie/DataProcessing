from Grammar_Tree import Tree
import json

data = json.load(open('27.json'))
tree = Tree(data['annotations'])

print(tree)