class Node:
    def __init__(self, prob=None, dataval=None):
        self.prob = prob
        self.dataval = dataval # 创建堆
        self.lastnode = None
        self.nextnode = None

class SLinkedList:
    def __init__(self):
        self.headnode = None

    def checkEmptyList(self):
        if self.headnode == None:
            print("EmptyList.")
            return

    def addNode(self, prob):
        if self.headnode == None:
            # 空表 --> 在头部插入节点
            self.headnode = Node(prob = prob)
        else:
            # 非空表 --> 选择合适位置插入
            type, node = self.getPosition(prob)
            if type == 'insertVal':
                pass
            else:
                self.Inbetween(node, prob)
    
    def getPosition(self, prob):
        self.checkEmptyList()
        node = self.headnode
        # return 1 添加值
        # return 0 添加新节点
        while node != None:
            if prob == node.prob:
                return 'insertVal',node
            elif node.nextnode == None:
                return 'insertNode',node
            elif prob < node.nextnode.prob:
                return 'insertNode',node
            node = node.nextnode

    def popMinElem(self):
        node = self.headnode.nextnode
        print(node.prob)

# Function to add node in 'middle_node'
    def Inbetween(self,middle_node,newdata):
        if middle_node is None:
            print("The mentioned node is absent")
            return

        NewNode = Node(newdata)
        NewNode.nextnode = middle_node.nextnode
        middle_node.nextnode = NewNode

# Print the linked list
    def listprint(self):
        printval = self.headnode
        while printval is not None:
            print (printval.prob)
            printval = printval.nextnode

if __name__ == '__main__':
    list = SLinkedList()
    list.headnode = Node(0) # 首节点
    e2 = Node(2)
    e3 = Node(5)

    list.headnode.nextnode = e2
    e2.nextnode = e3

    list.listprint()

    # ret = list.getPosition(100)
    # print(ret[0], ret[1].prob)
    # list.Inbetween(ret[1],100)
    list.addNode(100)
    
    list.listprint()

    list.popMinElem()