from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import *
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *

import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True

#config.quality = "low_quality"
config.quality = "medium_quality"
#config.quality = "high_quality"
#config.quality = "production_quality"
#config.quality = "fourk_quality"

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = False

    
    scene.changeRootPackingAndSorting(RootPacking.No_Packing, rootSorting=RootSorting.Heigth_Width, isAnimation=False)

    heap.isAnimation = True

    for i in range(5):
        heap.insert(i)

    heap.isAnimation = True
    
    heap.extract_min()

    #scene.changeTreeLayout(layout=TreeLayout.Balanced, isAnimation=True)
    
    scene.wait(2)
    
    #scene.changeTreeLayout(layout=TreeLayout.H_V, isAnimation=True)
    
    scene.wait(2)
    
    #cene.changeTreeLayout(layout=TreeLayout.RightAlligned, isAnimation=True)
    
    scene.wait(2)
    
    # #For adding bounds of trees
    # for i in scene.rootRects:
    #     r = Rectangle(height=i.h, width=i.w)
    #     r.move_to((i.x+(r.width/2), i.y-(r.height/2), -1))
    #     scene.add(r)

    # #For adding the bounds off the root packing:
    # x = Rectangle(height=scene.bounds[1], width=scene.bounds[0])
    # x.move_to((0+x.width/2, 0-x.height/2, 0))
    # scene.add(x)

    # scene.wait(3)
    
    # scene.changeTreeLayout(layout=TreeLayout.RightAlligned, isAnimation=True)
    
    # #For adding bounds of trees
    # for i in scene.rootRects:
    #     r = Rectangle(height=i.h, width=i.w)
    #     r.move_to((i.x+(r.width/2), i.y-(r.height/2), -1))
    #     scene.add(r)

    # #For adding the bounds off the root packing:
    # x = Rectangle(height=scene.bounds[1], width=scene.bounds[0])
    # x.move_to((0+x.width/2, 0-x.height/2, 0))
    # scene.add(x)

    #scene.wait(3)
    
    scene.render()
    print("--- %s seconds ---" % (time.time() - start_time))
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()