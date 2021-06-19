# -*- coding: utf-8 -*-

BIN_HEX = {'0000':'0', '0001':'1', '0010':'2', '0011':'3', '0100':'4', '0101':'5',
          '0110':'6', '0111':'7', '1000':'8', '1001':'9', '1010':'A', '1011':'B',
          '1100':'C', '1101':'D', '1110':'E', '1111':'F'}

def bin2hex(binVal):
    """ 
    bin2hex
    Args:
        binary text
    Returns: 
        hex text
    """
    output = ""
    bits = []
    length = len(binVal)
    if(length%4 != 0):
        for x in range(4-(length%4)):
            binVal += "0"
            length +=1
    for i in range(length//4):
        bits.append(binVal[i*4:(4 + (i*4))])
    for halfByte in bits:
        output+= BIN_HEX[halfByte]
    return output