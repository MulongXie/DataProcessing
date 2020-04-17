import numpy as np
from collections import Counter

class Rep_Identifier:
    def __init__(self, grammar_tree):
        self.sentences = grammar_tree.captions_encoded
        self.subtrees = grammar_tree.subtrees
        self.leaves = []
        self.subtree_map = {}

    def identify_leaves(self, level):
        non_leaves = []
        for subtree in self.subtrees:
            if subtree.count('{') == level:
                self.leaves.append(subtree)
            else:
                non_leaves.append(subtree)
        self.subtrees = non_leaves

    def update_subtrees(self):
        new_non_leaves = []
        for subtree in self.subtrees:
            for leaf in self.subtree_map:
                if leaf in subtree:
                    subtree = subtree.replace(leaf, self.subtree_map[leaf])
                    new_non_leaves.append(subtree)
        self.subtrees = new_non_leaves

    def apriori(self):
        level = 1

        while True:
            print(self.subtrees)
            self.identify_leaves(level)
            print(self.leaves)
            counter = Counter(self.leaves)
            print(counter)
            index = 0
            for subtree in counter:
                if counter[subtree] > 1:
                    self.subtree_map[subtree] = 'M' + str(index)
                    index += 1
            print(self.subtree_map)
            self.update_subtrees()
            print(self.subtrees)
            break


