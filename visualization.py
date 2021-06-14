
import tkinter as tk
import os

window = tk.Tk()
window.title("Huffman Tree Visualization")
window.geometry('1080x720')
sb = tk.Scrollbar(window)
canvas = tk.Canvas(window, bg="white", height=500, width=300, yscrollcommand=sb.set)
input_entry = tk.Entry(window, bd=2, font="Constaintia", width=30)


layers = [{'b': [0, 2, None, None], 'c': [1, 1, None, None], 'a': [2, 1, None, None]}, {'ac': [0, 2, [0, 'a'], [0, 'c']]}, {'abc': [0, 4, [1, 'ac'], [0, 'b']]}]
nodes = layers.copy()

size_oval = 14
pos_init_node = [15, 15]
distance_first_layer = 50
distance_line_y = 50
distance_layers = 100

canvas.delete('all')
canvas.create_line(0, 5, 1920, 5, width=5)

tag_list = []

# def plot():

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
            canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")
        else:
            x = pos_init_node[0] + distance_layers * num_layer
            last_node_a = nodes[layers[num_layer][key][2][0]][layers[num_layer][key][2][1]]
            last_node_b = nodes[layers[num_layer][key][3][0]][layers[num_layer][key][3][1]]
            y = abs(last_node_a[1] + last_node_b[1])/2
            canvas.create_oval(x - size_oval, y - size_oval, x + size_oval, y + size_oval, fill="yellow")
            # last_node_a 22222221
            #                    1
            #                    144444444 next_node
            #                    1
            # last_node_a 33333331
            canvas.create_line(x - distance_line_y, last_node_a[1], x - distance_line_y, last_node_b[1])    # line 1
            canvas.create_line(last_node_a[0], last_node_a[1], x - distance_line_y, last_node_a[1])    # line 2
            canvas.create_line(last_node_b[0], last_node_b[1], x - distance_line_y, last_node_b[1])    # line 3
            canvas.create_line(x - distance_line_y, y, x, y)    # line 4
        nodes[num_layer][key] = [x, y]

        tag_list.append(tk.Label(window, text=str(key), bg="white"))
        tag_list[len(tag_list) - 1].place(x=x+0-7, y=y+160-12)

        node_cnt += 1

def print_screen():
    pass

def main():
    global step
    # tk.Button(window, text='Go !', font="constantia", command=read).place(x=10, y=10)
    # tk.Button(window, text='Previous Step', font="constantia", command=previous_step).place(x=10, y=60)
    # tk.Button(window, text='Next Step', font="constantia", command=next_step).place(x=10, y=110)
    # tk.Label(window, text="Please input the weight of the nodes: ", font="constantia").place(x=200, y=30)
    input_entry.place(x=200, y=60)
    # print_screen()
    canvas.place(x=0, y=160)
    window.update()
    window.mainloop()


if __name__ == '__main__':
    main()