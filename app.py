from controller import Controller

def run():
    #SETUP 
    heap_controller = Controller()
    heap_controller.change_packing()
    
    node_to_decrease = None
    node_to_decrease_two = None

    for i in range(25):
        if i == 18:
            node_to_decrease = heap_controller.insert_node(i)
        elif i ==19:
            node_to_decrease_two = heap_controller.insert_node(i)
        else:
            heap_controller.insert_node(i)

    heap_controller.set_show_animations(True)
    heap_controller.extract_min()
    heap_controller.decrease_value(node_to_decrease, -1)
    heap_controller.decrease_value(node_to_decrease_two, 0)

    heap_controller.export_video()
     
run()