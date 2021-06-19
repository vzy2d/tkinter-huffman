# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk,messagebox,filedialog
import copy
import json
import os

from HuffmanEncoding import text2tree
from utils import bin2hex

class Application(Frame):
    """ GUI based-on Tkinter. """
    def __init__(self, master=None, default_text = '11100002234567'):
        super().__init__(master)
        self.master = master
        self.default_text = default_text
        self.grid()

        # 待编码内容输入
        ####################################
        
        # TODO add button for read text from system's file explorer
        Button(master, text='Read From File', command=self.read_text_from_file).grid(row=0, column=0, sticky=W)

        # 编码按钮
        Button(master, text='Encode', command=self.compute_and_display).grid(row=0, column=1, sticky=W)

        # 绘图按钮
        self.button_draw_graph = Button(master, text='Draw graph', command=self.graph_window)
        self.button_draw_graph.grid(row=0, column=1, sticky=E)

        # 待编码字符串输入框标题
        # label
        self.label_for_text  = Label(master, text ="Texte original" )
        self.label_for_text.grid(row=1, column=0, pady=(5,5))

        # 待编码字符串输入框
        # widget text
        self.text = Text(master, width=50, height=12.45)
        self.text.insert(END, self.default_text)
        self.text.grid(row=2, padx=10, pady=10)

        # 编码结果显示框 - 表格
        ##################################
        self.label_for_tree  = Label(master, text ="Results" )
        self.label_for_tree.grid(row=1, column=1, pady=(5,5))

        # table creation and formatting
        style = ttk.Style()
        style.configure("Treeview", font=('courier', 10))
        self.tree = ttk.Treeview(master, height=10)
        self.tree['show'] = 'headings' # do not display the first column included by default
        
        # column definition
        self.tree["columns"]=("symbol", "frequence", "code", "total_bits")
        
        self.tree.column("symbol", width=100)
        self.tree.column("frequence", width=100)
        self.tree.column("code", width=200)
        self.tree.column("total_bits", width=100)
        
        self.tree.heading("symbol", text="Symbol")
        self.tree.heading("frequence", text="Frequence")
        self.tree.heading("code", text="Code")
        self.tree.heading("total_bits", text="Total bits")
        
        self.tree.grid(row=2, rowspan=2, column=1)
        
        # 编码结果显示框 - 二进制码流
        ##################################

        self.label_for_binary_text = Label( master, width = 50, text = 'Text encoded by Huffman')
        self.label_for_binary_text.grid(row=4, column=1, pady=(25,10)) 

        self.text_binary = Text(master, width=50, height=10)
        self.text_binary.grid(row=5, column=1)

        # 编码结果显示框 - 十六进制
        ##################################

        self.label_for_compressed_text  = Label( master, width = 50, text = 'Text compressed')
        self.label_for_compressed_text.grid(row=4, column=0, pady=(25,10))

        self.text_compressed = Text(master, width=50, height=10)
        self.text_compressed.grid(row=5, column=0)

        # 多窗口
        self.flag_graph_window = IntVar(self.master, value=0)

    def read_text_from_file(self):
        """ 
        'Read From File'按钮回调函数，用于从文件中读取待编码字符串
        """
        # FolderPath = filedialog.askdirectory()
        FilePath = filedialog.askopenfilename()
        if os.path.exists(FilePath):
            with open(FilePath, 'r') as FILE:
                text = FILE.read()
                if text:
                    self.text.delete('1.0', END)
                    self.text.insert(END, text)
                else:
                    messagebox.showerror('Error', '文件为空')

    def compute_and_display(self):
        """ 
        编码并显示编码结果
        """
        self.tree.delete(*self.tree.get_children())
        self.text_compressed.delete('1.0', END)
        self.text_binary.delete('1.0', END)
        text = self.text.get(1.0, 'end-1c')
        
        if text:

            self.label_for_text.config(text='Text original in ASCII: {} Bytes'.format(len(text)))  
            
            matrix, layers = text2tree(text)

            huffman = {}
            text_compressed_total_bits = 0

            matrix.sort(key=lambda p:list(layers[0].keys()).index(p[0]))

            for row in matrix:
                huffman[row[0]] = row[2]
                text_compressed_total_bits += row[3]
                self.tree.insert('', 'end', values=row)
            
            self.text_binary.insert(END, ''.join([ huffman[char] for char in text]))
            self.label_for_binary_text.config(text='Text encoded by Huffman: {} bits'.format(len(self.text_binary.get(1.0, 'end-1c'))))

            # 二进制码流显示着色
            cnt = 0
            for i in range(0,2):
                char_huffman_len = len( huffman[ text[i] ] )
                self.text_binary.tag_add("huffman_{}".format(i), "1.{}".format(cnt), "1.{}".format(cnt+char_huffman_len))
                if i % 2:
                    self.text_binary.tag_config("huffman_{}".format(i), background="gray")
                else:
                    self.text_binary.tag_config("huffman_{}".format(i), background="lightblue")
                cnt += char_huffman_len

            self.text_compressed.insert(END, bin2hex(self.text_binary.get(1.0, 'end-1c')))
            self.label_for_compressed_text.config(text='Text compressed: {} Bytes'.format(len(self.text_compressed.get(1.0, 'end-1c'))//2))

            # save layer info
            json_str = json.dumps(layers)
            with open("log.json", 'w') as FILE:
                FILE.write(json_str)

        else:
            messagebox.showerror('Error', '要压缩的文本不能为空或包含特殊字符')
            self.text.insert(END, "ascii only！")
    

    def draw_graph(self, layers):
        """ Draw graph in second window
            TODO add button for show 0/1 in the corner
        Args:
            layers
        Returns: 
        """
        nodes = copy.deepcopy(layers)

        size_oval = 14
        pos_init_node = [20, 30]
        distance_first_layer = 50
        distance_line_y = 50
        distance_layers = 100

        self.canvas.delete('all')
        self.canvas.create_line(0, 5, 1920, 5, width=5)

        tag_list = []

        for elem in tag_list:
            elem.destroy()
        tag_list = []
        for num_layer in range(len(layers)):
            node_cnt = 0
            for key in layers[num_layer]:
                if num_layer == 0:
                    x = pos_init_node[0]
                    y = pos_init_node[1] + distance_first_layer * node_cnt
                    self.canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")
                else:
                    x = pos_init_node[0] + distance_layers * num_layer
                    last_node_a = nodes[layers[num_layer][key][2][0]][layers[num_layer][key][2][1]]
                    last_node_b = nodes[layers[num_layer][key][3][0]][layers[num_layer][key][3][1]]
                    y = abs(last_node_a[1] + last_node_b[1])/2

                    # self.canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")

                    # 绘制连线
                    # last_node_a 22222221
                    #                    1
                    #                    144444444 next_node
                    #                    1
                    # last_node_a 33333331
                    self.canvas.create_line(x - distance_line_y, last_node_a[1], x - distance_line_y, last_node_b[1])    # line 1
                    self.canvas.create_line(last_node_a[0], last_node_a[1], x - distance_line_y, last_node_a[1])    # line 2
                    self.canvas.create_line(last_node_b[0], last_node_b[1], x - distance_line_y, last_node_b[1])    # line 3
                    self.canvas.create_line(x - distance_line_y, y, x, y)    # line 4
                nodes[num_layer][key] = [x, y]

                if num_layer == 0:
                    bg = "yellow"
                else:
                    bg = "white"
                tag_list.append(Label(self.win_graph_master, text=str(key), bg=bg))
                tag_list[len(tag_list) - 1].place(x=x-7, y=y-12)

                node_cnt += 1
    
    def graph_window(self):
        """ 
        绘制第二窗口用于显示计算图
        """
        if os.path.exists("log.json"):
            with open("log.json", 'r') as FILE:
                layers = json.load(FILE)
                if self.flag_graph_window.get()==0:
                    self.flag_graph_window.set(1)
                    
                    # setting new window
                    window_width = min(1200, len(layers) * 100 + 10)
                    window_height = min(800, len(layers[0]) * 50 + 30-20)
                    self.win_graph_master = Toplevel(self.master, width=window_width, height=window_height)
                    self.win_graph_master.title('graph')
                    self.win_graph_master.attributes('-topmost', 1)

                    # 编码结果 - 图
                    ##################################
                    self.canvas = Canvas(self.win_graph_master, bg="white", height=1080, width=1920)
                    self.canvas.place(x=0, y=0)
                    self.draw_graph(layers)

                    self.button_draw_graph.wait_window(self.win_graph_master)
                    self.flag_graph_window.set(0)
        else:
            print("log file not exist!")
            return




if __name__ == "__main__":
    root = Tk()
    root.config(bd=10)
    root.option_add("*Font", "courier")
    root.wm_title('Huffman')
    root.minsize(width=666, height=600)
    root.resizable(width=False, height=False)

    # 推出graprightque界面
    txt =  'HHHHDDDDDEEEEEEGGGGGGGFFFFFFFFFFAAAAAAAAAABBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'
    # txt =  '00001112234567'
    # txt =  'statetree'

    app = Application(master=root, default_text=txt)
    app.mainloop()