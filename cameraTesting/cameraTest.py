from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import *
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *
import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True
config.media_dir = "./cameraTesting/media"
config.quality = "low_quality"

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Right aligned
    scene.treeLayout = TreeLayout(1)

    #Balanced
    #scene.treeLayout = TreeLayout(2)

    #H_V
    #scene.treeLayout = TreeLayout(3)
    
    # Currently checking
    scene.changeRootPackingAndSorting(RootPacking.No_Packing, rootSorting=RootSorting.Order, isAnimation=False)
    #scene.changeRootPackingAndSorting(RootPacking.No_Packing, rootSorting=RootSorting.Heigth_Width, isAnimation=False)
    #scene.changeRootPackingAndSorting(RootPacking.Binary_Tree_Packing, rootSorting=RootSorting.Order, isAnimation=False)
    #scene.changeRootPackingAndSorting(RootPacking.Binary_Tree_Packing, rootSorting=RootSorting.Heigth_Width, isAnimation=False)
    #scene.changeRootPackingAndSorting(RootPacking.FFDH, rootSorting=RootSorting.Order, isAnimation=False)
    #scene.changeRootPackingAndSorting(RootPacking.FFDH, rootSorting=RootSorting.Heigth_Width, isAnimation=False)

    #Set animation 
    heap.isAnimation = False
    scene.display_custom_text("we insert 32 nodes")
    for i in range(12, 0, -1):
        heap.insert(i)

    heap.isAnimation = True
    heap.extract_min()
    heap.showExplanatoryText = True
    heap.decrease_value(7, -1)

    # heap.isAnimation = False
    # scene.display_custom_text("we will now insert 32 nodes more")
    # for i in range(32):
    #     heap.insert(i)
    
    #scene.display_custom_text("hello we will insert 32 nodes more")

    # heap.isAnimation = True
    # heap.showExplanatoryText = True
    # heap.extract_min()
  
    # scene.remove(x)
    # for i in scene.rootRects:
    #     r = Rectangle(height=i.h, width=i.w)
    #     r.move_to((i.x+(r.width/2), i.y-(r.height/2), -1))
    #     scene.add(r)

    scene.render()
    print("--- %s seconds ---" % (time.time() - start_time))
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()
