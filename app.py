from controller import Controller

def run():
    #SETUP 
    heap_controller = Controller()
    #heap_controller.change_packing()
    heap_controller.isAnimation = True



    for i in range(30):
        heap_controller.insert_node(i)
    
    heap_controller.extract_min()
        
    heap_controller.export_video()
run()