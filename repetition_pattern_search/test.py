
def hierarchy(sentence):
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
            print(start_node, sentence[start_p:end_p + 1])
        elif c is ' ':
            pass
        else:
            node += c
            continue

        if node != '':
            nodes.append(node)
            node = ''
    print(nodes)


def build_hie(sentence):
    print(sentence)
    subtree = {}
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
            if start_node not in subtree:
                subtree[start_node] = build_hie(sentence[start_p + 1:end_p])
            else:
                subtree[start_node] += build_hie(sentence[start_p + 1:end_p])

            print(subtree)
        elif c is not ' ':
            node += c
            if i == len(sentence) - 1:
                nodes.append(node)
            continue

        if node != '':
            nodes.append(node)
            node = ''
    if len(subtree)==0:
        subtree = nodes
    return subtree

tree = {}
s = '4{0{1{5 5} 0{3}}} '
hierarchy(s)
# build_hie(s)