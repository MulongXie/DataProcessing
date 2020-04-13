import numpy as np
from collections import Counter

class Rep_Identifier:
    def __init__(self, grammar_tree):
        self.sentences = grammar_tree.captions_encoded
        self.subtrees = grammar_tree.subtrees
        self.leaves = []
        self.non_leaves = []
        self.subtree_map = {}
        self.identify_leaves()

    def identify_leaves(self):
        for subtree in self.subtrees:
            if subtree.count('{') == 1:
                self.leaves.append(subtree)
            else:
                self.non_leaves.append(subtree)
        print(self.leaves)

    def update_subtrees(self):
        new_non_leaves = []
        for subtree in self.non_leaves:
            for leaf in self.subtree_map:
                if leaf in subtree:
                    subtree = subtree.replace(leaf, self.subtree_map[leaf])
                    new_non_leaves.append(subtree)
        self.non_leaves = new_non_leaves

    def apriori(self):
        counter = Counter(self.leaves)
        index = 0
        for subtree in counter:
            if counter[subtree] > 1:
                self.subtree_map[subtree] = 'M' + str(index)
                index += 1
        print(self.subtree_map)

        self.update_subtrees()
        print(self.non_leaves)

