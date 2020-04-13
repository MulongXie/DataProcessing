import re


class Tree:
    def __init__(self, annotations):
        self.vocabulary = None
        self.token_set = set()
        self.token_map = {}
        self.token_count = {}
        self.caption = annotations
        self.subtrees = []
        self.subtrees_encoded = []
        self.build_tree()

    def build_tree(self):
        for cap in self.caption:
            self.subtrees.append(cap['caption'])
        self.get_tokens()
        self.encode_subtree()

    def tokenize(self, line):
        tokens_temp = re.split('[ {}]', line)
        tokens = []
        for t in tokens_temp:
            if t != '':
                tokens.append(t)
                self.token_set.add(t)
        symbol_count = line.count('{')
        for i in range(symbol_count):
            tokens += ['{', '}']
        return tokens

    def get_tokens(self):
        for subtree in self.subtrees:
            tokens = self.tokenize(subtree)
            for token in tokens:
                self.token_count[token] = self.token_count.get(token, 0) + 1
        for i, token in enumerate(self.token_set):
            if token not in ['{', '}']: self.token_map[token] = str(i)

    def encode_subtree(self):
        for subtree in self.subtrees:
            token = ''
            subtree_encode = ''
            for c in subtree:
                if c in ['{', '}', ' ']:
                    if token != '':
                        subtree_encode += self.token_map[token] + c
                        token = ''
                    else:
                        subtree_encode += c
                    continue
                token += c
            self.subtrees_encoded.append(subtree_encode)
