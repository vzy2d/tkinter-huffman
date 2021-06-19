# -*- coding: utf-8 -*-
class zyheap():
    '''a heap for huffman enconding'''
    def __init__(self):
        self.heap = []
        self.__flag_refreshed = False

    def __del__(self):
        pass    

    def pop(self):
        '''pop an elements from heap'''
        return self.heap.pop(0)

    def push(self, elem):
        '''push an elements to heap'''
        self.heap.append(elem)
        self.__sort()

    #heap elems sort
    def __sort(self):
        '''heap elements sort'''
        self.heap.sort(key=lambda p:p[0])
        div = []
        cnt = 0
        div.append([])
        for val in self.heap:
            if len(div[cnt]) == 0:
                div[cnt].append(val)
            elif val[0] == div[cnt][0][0]:
                div[cnt].append(val)
            else:
                div.append([])
                div[cnt+1].append(val)
                cnt += 1
        self.heap = []
        for i in range(len(div)):
            if len(div[i]) > 1:
                if self.__flag_refreshed == False:
                    div[i].sort(key=lambda p:p[2][0], reverse=True)
                else:
                    div[i].sort(key=lambda p:p[1], reverse=True)
            for j in range(len(div[i])):
                self.heap.append(div[i][j])

    def refreshPositionInfo(self):
        '''refresh Position Info in self.heap[x][1]'''
        if self.__flag_refreshed == True:
            print('refreshed')
            return
        else:
            self.flag_refreshed = True
            for i in range(1,len(self.heap)+1):
                self.heap[-i][1] = i-1

    def show(self):
        '''print all elements of heap'''
        for i in range(len(self.heap)):
            print(self.heap[i])

if __name__ == "__main__":
    symb2freq = {'C': 40, 'B': 18, 'F': 10, 'A': 10, 'G': 7, 'E': 6, 'D': 5, 'H': 4}
    print(symb2freq)

    elems = [[wt, 0, [sym, ""]] for sym, wt in symb2freq.items()]

    heap = zyheap(False)
    for i in range(len(elems)):
        heap.push(elems[i])

    heap.refreshPositionInfo()

    for i in range(len(elems)):
        print(heap.pop())
    