from controller import Controller

def run():
    #SETUP 
    heap_controller = Controller()
    heap_controller.isAnimation = False
    nodes = []

#For video 1-3
    heap_controller.change_tree_layout(1, animate=False,isColor=False)
    heap_controller.change_tree_layout(2, animate=False,isColor=False)
    heap_controller.change_tree_layout(3, animate=False,isColor=False)
    #1
    for n in range(33):
        nodes.append(heap_controller.insert(n))
    heap_controller.wait(2)   
    # 2
    heap_controller.extract_min()
    heap_controller.wait(1)   
    heap_controller.extract_min()
    heap_controller.wait(2) 
    # 3
    heap_controller.isAnimation = False
    for n in range(98):
        nodes.append(heap_controller.insert(n))
    heap_controller.extract_min()
    heap_controller.isAnimation = True
    heap_controller.decrease_value(nodes[69],2)
    heap_controller.decrease_value(nodes[101],3)
    heap_controller.decrease_value(nodes[117],4)
    heap_controller.decrease_value(nodes[125],5) 
    heap_controller.decrease_value(nodes[128],6)
    heap_controller.decrease_value(nodes[129],7) 

#For Video 4-6
    #heap_controller.change_tree_layout(1, animate=False,isColor=False)
    #heap_controller.change_tree_layout(2, animate=False,isColor=False)
    #heap_controller.change_tree_layout(3, animate=False,isColor=False)

    # for n in range(513):
    #     nodes.append(heap_controller.insert(n))
    # heap_controller.extract_min()
    # heap_controller.decrease_value(nodes[2],0)
    # heap_controller.decrease_value(nodes[3],0)
    # heap_controller.decrease_value(nodes[5],0)
    # heap_controller.decrease_value(nodes[9],0) 
    # heap_controller.decrease_value(nodes[17],0)
    # heap_controller.decrease_value(nodes[33],0) 
    # heap_controller.decrease_value(nodes[65],0) 
    # heap_controller.decrease_value(nodes[129],0) 
    # heap_controller.decrease_value(nodes[257],0) 
    # heap_controller.isAnimation = True

    ## 1
    # heap_controller.change_packing_and_sorting(1,1, animate=True)
    # heap_controller.wait(2)   
    # heap_controller.change_packing_and_sorting(1,2, animate=True)
    # heap_controller.wait(2)   
    # heap_controller.change_packing_and_sorting(1,1, animate=True)
    # heap_controller.wait(2)   
    ## 2
    # heap_controller.change_packing_and_sorting(2,1, animate=True)
    # heap_controller.wait(2)   
    # heap_controller.change_packing_and_sorting(2,2, animate=True)
    # heap_controller.wait(2)   
    ## 3
    ## heap_controller.change_packing_and_sorting(3,1, animate=True)
    ## heap_controller.wait(2)   
    ## heap_controller.change_packing_and_sorting(3,2, animate=True)

#For video 7
    # for n in range(512):
    #     nodes.append(heap_controller.insert(n))
    # heap_controller.extract_min()

    # heap_controller.isAnimation = True

    # heap_controller.change_tree_layout(2, animate=True,isColor=False)
    # heap_controller.wait(2) 
    # heap_controller.change_tree_layout(3, animate=True,isColor=False)
    # heap_controller.wait(2) 
    # heap_controller.change_tree_layout(2, animate=True,isColor=False)
    # heap_controller.wait(2) 
    # heap_controller.change_tree_layout(1, animate=True,isColor=False)
    # heap_controller.wait(2) 
    # heap_controller.change_tree_layout(3, animate=True,isColor=True)
    # heap_controller.wait(2) 
    # heap_controller.change_tree_layout(1, animate=True,isColor=False)
    # heap_controller.wait(2) 






    heap_controller.export_video()
run()