from controller import Controller

def run():
    #SETUP 
    heap_controller = Controller()
    heap_controller.change_packing()

    for i in range(9):
        if i == 4:
            x = heap_controller.insert_node(i)
        else:
            heap_controller.insert_node(i)

    heap_controller.set_show_animations(True)
    heap_controller.extract_min()
    heap_controller.decrease_value(x, -1)
    heap_controller.extract_min()
    heap_controller.extract_min()

    heap_controller.export_video()
     
run()