from controller import Controller
import time
def run():
    #SETUP 
    heap_controller = Controller()
    heap_controller.set_show_animations(True)
    start = time.time()
    for i in range(16):
        heap_controller.insert(i)
    
    #heap_controller.change_packing_and_sorting(3, 2)
    heap_controller.change_tree_layout(3)
    heap_controller.extract_min()
    # for i in range(15):
    #     if i == 7:
    #         x = heap_controller.insert(i)
    #     else:
    #         heap_controller.insert(i)

    # heap_controller.change_packing_and_sorting(1, 2)

    # heap_controller.extract_min()
    # heap_controller.delete(x)
    heap_controller.export_video()
    end = time.time()
    print(end-start)
run()