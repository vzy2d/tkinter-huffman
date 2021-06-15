# -*- coding: utf-8 -*-
from heapq import heappush, heappop, heapify
import collections

def get_new_text(node):
    new_text = ''
    if len(node) > 2:
        for i in range(1, len(node)):
            new_text += node[i][0]
        return "".join(sorted(new_text))
    else:
        return node[1][0]


def huffman_encoding(symb2freq):
    """ Encodage des characteres selon la technique de Huffman.
        Retourne une liste dont chaque element est une liste de la forme [caractere, code de Huffman] 
        Utilisation d'un tas pour faciliter la manipulation des donnees. 
    """
    step = 0
    nodes = []
    lines = []
    numbers = []
    layers = []
    
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    
    # transformation de la liste en tas pour facilier la manipulation des donnees
    heapify(heap)
    
    seq = sorted(heap, reverse=True)
    layer = dict()
    text_dict = dict()  # 记录节点所在层
    for i in range(len(seq)):
        layer[seq[i][1][0]] = [i,seq[i][0],None,None] #[No., Prob, next_node_a, next_node_b]
        text_dict[seq[i][1][0]] = 0 # text belone to which layer
    layers.append(layer.copy())
    
    layer.clear()
    step += 1
    while len(heap) > 1:
        
        left = heappop(heap)
        right = heappop(heap)
        # next_node_a [layer, node num]
        # next_node_b
        left_text = get_new_text(left)
        right_text = get_new_text(right)
        new_text = "".join(sorted(left_text + right_text))
        layers.append({new_text : [0, left[0]+right[0], \
                [text_dict[left_text],  left_text], \
                [text_dict[right_text], right_text]]})
        text_dict[new_text] = step
        step += 1
        
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        
        heappush( heap, [ left[0] + right[0] ] + left[1:] + right[1:] )
        print(heap,'\n')
    print(layers, len(layers))
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p)), layers


def text2tree(txt):
    """ Retourne une liste de tuple ordonnée du poids le plus fort (plus forte probabilite d'occurence) au poids le plus faible.
        Un element de liste contient un tuple de la forme (symbole, poids, code de Huffman). 
    """
    
    symb2freq = collections.Counter(txt)
    huff, layers = huffman_encoding(symb2freq)
    print(huff)
    
    return [ ( p[0], symb2freq[p[0]], p[1], int(symb2freq[p[0]])*len(p[1]) ) for p in huff ], layers

if __name__ == "__main__":

    txt = 'ascii only!'
    symb2freq = collections.Counter(txt)
    print(symb2freq)
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    print(heap)

    tree = text2tree(txt)
