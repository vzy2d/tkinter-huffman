# -*- coding: utf-8 -*-
import collections
import copy

from zyheap import zyheap

def get_new_text(node):
    """ 
    合并子节点字符
    """
    new_text = ''
    if len(node) > 3:
        for i in range(2, len(node)):
            new_text += node[i][0]
        return "".join(sorted(new_text))
    else:
        return node[2][0]

def huffman_encoding(symb2freq):
    """ 

    Args:
        symb2freq
    Returns: 
        sorted(heap.pop()[2:], key=lambda p: (len(p[-1]), p))：编码结果
        layers：计算图信息，用于可视化
    """
    step = 0
    layers = []
    
    elems = [[wt, 0, [sym, ""]] for sym, wt in symb2freq.items()]
    
    heap = zyheap()
    for i in range(len(elems)):
        heap.push(elems[i])

    heap.refreshPositionInfo()

    layer = dict()
    text_dict = dict()  # 记录节点所在层
    for i in range(1,len(heap.heap)+1):
        layer[heap.heap[-i][2][0]] = [i-1,heap.heap[-i][0],None,None] #[No., Prob, next_node_a, next_node_b]
        text_dict[heap.heap[-i][2][0]] = 0 # record text belone to which layer
    layers.append(copy.deepcopy(layer))
    
    layer.clear()
    step += 1
    while len(heap.heap) > 1:
        
        left = heap.pop()
        right = heap.pop()
        # next_node_a [layer, node num] --> [layer, node num, position_vertical]
        # next_node_b
        left_text = get_new_text(left)
        right_text = get_new_text(right)
        new_text = "".join(sorted(left_text + right_text))
        layers.append({new_text : [0, left[0]+right[0], \
                [text_dict[left_text],  left_text], \
                [text_dict[right_text], right_text]]})
        text_dict[new_text] = step
        step += 1
        
        for pair in left[2:]:
            pair[1] = '1' + pair[1]
        
        for pair in right[2:]:
            pair[1] = '0' + pair[1]
        
        heap.push([ left[0] + right[0] ] + [ (left[1] + right[1])/2 ] + left[2:] + right[2:] )
    return sorted(heap.pop()[2:], key=lambda p: (len(p[-1]), p)), layers


def text2tree(txt):
    
    symb2freq = collections.Counter(txt)
    huff, layers = huffman_encoding(symb2freq)
    
    return [ ( p[0], symb2freq[p[0]], p[1], int(symb2freq[p[0]])*len(p[1]) ) for p in huff ], layers


if __name__ == "__main__":

    txt =  'HHHHDDDDDEEEEEEGGGGGGGFFFFFFFFFFAAAAAAAAAABBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'
    txt =  'statetree'
    
    symb2freq = collections.Counter(txt)
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]

    print(sorted(heap, key=lambda p:(p[0], p[1][0])))

    # heap.sort(reverse=True)
    
    seq = sorted(heap, reverse=True)

    tree = text2tree(txt)