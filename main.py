# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import json
import os

from HuffmanEncoding import text2tree
from utils import bin2hexa

class Application(Frame):
    """ GUI based-on Tkinter. """

    def __init__(self, master=None):
        
        super().__init__(master)
        self.master = master
        self.grid()

        # titre de l'application
        Label(master, text='La compression de Huffman', font="courier 14 bold").grid(row=0, columnspan=3, pady=(0,20))

        # 待编码内容输入
        ####################################
        
        # 待编码字符串输入框标题
        # label
        self.label_for_text  = Label(master, text ="Texte original" )
        self.label_for_text.grid(row=1, column=0, pady=(5,5))

        # 待编码字符串输入框
        # widget text
        self.text = Text(master, width=50, height=10)
        self.text.insert(END, "ascii only!")
        self.text.grid(row=2, padx=10, pady=10)

        # 编码按钮
        Button(master, text='Compresser le texte', command=self.compute_and_display).grid(row=3)

        # 测试按钮
        self.button_draw_graph = Button(master, text='Draw graph', command=self.graph_window).grid(row=4)

        # 编码结果 - 表格
        ##################################

        # label du panel
        self.label_for_tree  = Label(master, text ="Details de l'encodage" )
        self.label_for_tree.grid(row=1, column=1, pady=(5,5))

        # creation et mise en forme du tableau
        style = ttk.Style()
        style.configure("Treeview", font=('courier', 10))
        self.tree = ttk.Treeview(master, height=10)
        ysb = ttk.Scrollbar(master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        self.tree['show'] = 'headings' # ne pas afficher la premiere colonne incluse par defaut
        
        # definition des colonnes
        self.tree["columns"]=("symbole", "frequence", "code", "total_bits")
        
        self.tree.column("symbole", width=100)
        self.tree.column("frequence", width=100)
        self.tree.column("code", width=200)
        self.tree.column("total_bits", width=100)
        
        self.tree.heading("symbole", text="Symbole")
        self.tree.heading("frequence", text="Fréquence")
        self.tree.heading("code", text="Code")
        self.tree.heading("total_bits", text="Total bits")
        
        self.tree.grid(row=2, rowspan=2, column=1)
        ysb.grid(row=2, rowspan=2, column=2)
        
        # 编码结果 - 二进制码流
        ##################################

        self.label_for_binary_text      = Label( master, width = 50, text = 'Text encode by Huffman')
        self.label_for_binary_text.grid(row=4, column=1, pady=(25,10)) 

        self.text_binary = Text(master, width=50, height=10)
        self.text_binary.grid(row=5, column=1)

        # 编码结果 - 十六进制
        ##################################

        self.label_for_compressed_text  = Label( master, width = 50, text = 'Text compresse')
        self.label_for_compressed_text.grid(row=4, column=0, pady=(25,10))

        self.text_compressed = Text(master, width=50, height=10)
        self.text_compressed.grid(row=5, column=0)

        # 多窗口
        self.flag_graph_window = IntVar(self.master, value=0)


    def compute_and_display(self):
        
        # reset des vues affichant les resultats d'encodage
        self.tree.delete(*self.tree.get_children())
        self.text_compressed.delete('1.0', END)
        self.text_binary.delete('1.0', END)
        text = self.text.get(1.0, 'end-1c') # peut etre vide si presence de caracteres speciaux sur certaines plateformes !
        
        if text:

            self.label_for_text.config(text='Texte original in ASCII: {} Bytes'.format(len(text)))  
            
            matrix, layers = text2tree(text)

            huffman = {}
            text_compressed_total_bits = 0

            for row in matrix:
                # creation d'un dictionnaire pour convertir facilement un caractere en son code de Huffman
                huffman[row[0]] = row[2]
                # cacul du nombre total de bits utilises pour encoder le texte selon Huffman
                text_compressed_total_bits += row[3]
                # mise a jour de l'affichage de l'arbre avec les resultats du calcul
                self.tree.insert('', 'end', values=row)
            
            # mise a jour de l'affichage du panel sud ouest avec le texte encode selon Huffamen et son label indiquant le nombre de caractere 
            
            self.text_binary.insert(END, ''.join([ huffman[char] for char in text]))
            self.label_for_binary_text.config(text='Text encoded by Huffman: {} bits'.format(len(self.text_binary.get(1.0, 'end-1c'))))
            

            # surlignage des 2 premiers caracteres de Huffman pour aider a la comprehension de l'utilisateur

            char_1_huffman_len = len( huffman[ text[0] ] )
            char_2_huffman_len = len( huffman[ text[1] ] )

            self.text_binary.tag_add("huffman_1", "1.0", "1.{}".format(char_1_huffman_len))
            self.text_binary.tag_config("huffman_1", background="yellow")

            self.text_binary.tag_add("huffman_2", "1.{}".format(char_1_huffman_len), "1.{}".format(char_1_huffman_len+char_2_huffman_len))
            self.text_binary.tag_config("huffman_2", background="lightblue")


            # mise a jour de l'affichage du panel sud ouest avec le texte compresse (coversion du texte binaire en texte hexadecimal)

            self.text_compressed.insert(END, bin2hexa(self.text_binary.get(1.0, 'end-1c')))
            self.label_for_compressed_text.config(text='Texte compresse: {} octets'.format(len(self.text_compressed.get(1.0, 'end-1c'))//2))

            # save layer info
            json_str = json.dumps(layers)
            with open("log.json", 'w') as FILE:
                FILE.write(json_str)

        else:
            # il a ete constate que certaines plateformes ne supportent pas les caracteres speciaux dans le champs texte !
            messagebox.showerror('Error', '要压缩的文本不能为空或包含特殊字符')
            self.text.insert(END, "仅支持ascii字符！")
    
    def draw_graph(self, layers):
        nodes = layers.copy()

        size_oval = 14
        pos_init_node = [20, 30]
        distance_first_layer = 50
        distance_line_y = 50
        distance_layers = 100

        self.canvas.delete('all')
        self.canvas.create_line(0, 5, 1920, 5, width=5)

        tag_list = []

        # def plot():
        print(self.canvas.grid_info())
        for elem in tag_list:
            elem.destroy()
        tag_list = []
        for num_layer in range(len(layers)):
            node_cnt = 0
            for key in layers[num_layer]:
                print(num_layer, key)
                if num_layer is 0:
                    x = pos_init_node[0]
                    y = pos_init_node[1] + distance_first_layer * node_cnt
                    self.canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")
                else:
                    x = pos_init_node[0] + distance_layers * num_layer
                    last_node_a = nodes[layers[num_layer][key][2][0]][layers[num_layer][key][2][1]]
                    last_node_b = nodes[layers[num_layer][key][3][0]][layers[num_layer][key][3][1]]
                    y = abs(last_node_a[1] + last_node_b[1])/2

                    # self.canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")

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

                if num_layer is 0:
                    bg = "yellow"
                else:
                    bg = "white"
                tag_list.append(Label(self.win_graph_master, text=str(key), bg=bg))
                tag_list[len(tag_list) - 1].place(x=x-7, y=y-12)

                node_cnt += 1
    
    def graph_window(self):
        """ 
        setting for second window
        """
        if os.path.exists("log.json"):
            with open("log.json", 'r') as FILE:
                layers = json.load(FILE)
                if self.flag_graph_window.get()==0:
                    self.flag_graph_window.set(1)
                    # setting new window
                    # w1 = myWindow(root, 'First Window', 1)
                    self.win_graph_master = Toplevel(self.master, width=500, height=300)
                    self.win_graph_master.title('graph')
                    self.win_graph_master.attributes('-topmost', 1)

                    # 编码结果 - 图
                    ##################################
                    self.canvas = Canvas(self.win_graph_master, bg="white", height=1080, width=1920)
                    self.canvas.place(x=0, y=0)
                    self.draw_graph(layers)
                    # FIXME: AttributeError: 'NoneType' object has no attribute 'wait_window'
                    self.button_draw_graph.wait_window(self.win_graph_master)
                    self.flag_graph_window.set(0)
        else:
            print("log file not exist!")
            return




if __name__ == "__main__":
    root = Tk()
    # 格式化主窗口
    root.config(bd=10)
    root.option_add("*Font", "courier")
    root.wm_title('Huffman')
    root.minsize(width=666, height=600)
    root.resizable(width=False, height=False)

    # 推出graprightque界面
    app = Application(master=root)
    app.mainloop()