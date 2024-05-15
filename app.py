from controller import Controller
import time
import random

def run():
    #SETUP 
    heap_controller = Controller()
    heap_controller.isAnimation = False
    nodes = []
    for n in range(1025):#(4097):
        nodes.append(heap_controller.insert(n))

    heap_controller.extract_min()
    heap_controller.change_tree_layout(2,animate=True)
    heap_controller.wait(5)
    heap_controller.change_tree_layout(3,animate=True,isColor=False)
    heap_controller.change_tree_layout(3,animate=True,isColor=True)


    # heap_controller.decrease_value(nodes[30],2)
    # heap_controller.decrease_value(nodes[27],3)
    # heap_controller.decrease_value(nodes[18],4)
    # heap_controller.decrease_value(nodes[31],5) 



    # dc_nodes = []
    # delete_node = None

    # for i in range(16):
    #     if i == 10:
    #         dc_nodes.append(heap_controller.insert(i))
    #     else:
    #         heap_controller.insert(i)

    # heap_controller.extract_min()
    
    # for i in range(18):
    #     if i == 3 or i == 12 or i == 15 or i == 16:
    #         dc_nodes.append(heap_controller.insert(i+16))
    #     elif i == 11:
    #         delete_node = heap_controller.insert(i+16)
    #     else:
    #         heap_controller.insert(i+16)
    
    # heap_controller.extract_min()

    # for n in dc_nodes:
    #     if n.value == 10:
    #         heap_controller.decrease_value(n, 9)
    #     else:
    #         heap_controller.decrease_value(n, n.value-19)
    
    # heap_controller.delete(delete_node)
    # heap_controller.export_video()
    heap_controller.export_video()
run()