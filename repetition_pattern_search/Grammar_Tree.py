import re


class Tree:
    def __init__(self, annotations):
        self.annotations = annotations
        self.token_set = set()
        self.token_map = {}
        self.token_count = {}
        self.captions = []
        self.captions_encoded = []
        self.subtrees = []
        self.build_tree()

    def build_tree(self):
        for ann in self.annotations:
            self.captions.append(ann['caption'])
        self.get_tokens()
        self.encode_subtree()
        self.divide_subtrees()

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
        for cap in self.captions:
            tokens = self.tokenize(cap)
            for token in tokens:
                self.token_count[token] = self.token_count.get(token, 0) + 1
        for i, token in enumerate(self.token_set):
            if token not in ['{', '}']: self.token_map[token] = str(i)

    def encode_subtree(self):
        for cap in self.captions:
            token = ''
            subtree_encode = ''
            for c in cap:
                if c in ['{', '}', ' ']:
                    if token != '':
                        subtree_encode += self.token_map[token] + c
                        token = ''
                    else:
                        subtree_encode += c
                    continue
                token += c
            self.captions_encoded.append(subtree_encode)

    def divide_subtrees(self):
        for sentence in self.captions_encoded:
            node = ''
            nodes = []
            start_nodes = []
            start_pos = []
            for i, c in enumerate(sentence):
                if c is '{':
                    start_nodes.append(node)
                    start_pos.append(i)
                elif c is '}':
                    start_node = start_nodes.pop()
                    start_p = start_pos.pop()
                    end_p = i
                    self.subtrees.append(start_node+sentence[start_p:end_p + 1])
                elif c is ' ':
                    pass
                else:
                    node += c
                    continue

                if node != '':
                    nodes.append(node)
                    node = ''
