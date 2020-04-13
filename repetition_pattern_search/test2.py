import json

def hierarchy(sentence):
    subtree = []

    node = ''
    nodes = []

    start_nodes = []
    start_pos = []
    is_leaf = False
    for i, c in enumerate(sentence):
        if c is '{':
            start_nodes.append(node)
            start_pos.append(i)
            is_leaf = True
        elif c is '}':
            start_node = start_nodes.pop()
            start_p = start_pos.pop()
            end_p = i

            if is_leaf:
                subtree.append({start_node: sentence[start_p + 1:end_p].split(' ')})
            else:
                subtree = [{start_node: subtree}]
            is_leaf = False
            print(subtree)
            print(start_node, sentence[start_p:end_p + 1])
        elif c is not ' ':
            node += c
            if i == len(sentence) - 1:
                nodes.append(node)
            continue

        if node != '':
            nodes.append(node)
            node = ''
    print(nodes)


tree = {}
s = '4{0{2 1{5 5} 0{3}} 1{0} 2} '
hierarchy(s)
# build_hie(s)