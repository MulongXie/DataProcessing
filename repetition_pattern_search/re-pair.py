from Grammar_Tree import Tree
from Repetition_Identifier import Rep_Identifier as Idf
import json
from collections import Counter


data = json.load(open('27.json'))
tree = Tree(data['annotations'])

print(tree.token_map)
for i in range(len(tree.captions)):
    print(tree.captions[i])
    print(tree.captions_encoded[i])

idf = Idf(tree)
idf.apriori()