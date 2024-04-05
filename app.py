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

    scene.add(Dot(point=(0.0, -1.0, 0.0), color=PURPLE))
    #scene.changeRootPackingAndSorting(RootPacking.Binary_Tree_Packing, isAnimation=False)

    heap.isAnimation = True
    
    scene.add()

    for i in range(16):
        heap.insert(i)

    heap.extract_min()

    heap.isAnimation = True

    # scene.changeRootPackingAndSorting(rootSorting=RootSorting.Heigth_Width, isAnimation=True)

    # scene.zoom_out(True, scene.camera.frame_center, scene.camera.frame_width*1.5)
    # scene.wait(3)
    
    # scene.changeRootPackingAndSorting(rootPacking=RootPacking.FFDH, isAnimation=True)

    # #For adding bounds of trees
    # # for i in scene.rootRects:
    # #     r = Rectangle(height=i.h, width=i.w)
    # #     r.move_to((i.x+(r.width/2), i.y-(r.height/2), -1))
    # #     scene.add(r)

    # #For adding the bounds off the root packing:
    # # x = Rectangle(height=scene.bounds[1], width=scene.bounds[0])
    # # x.move_to((0+x.width/2, 0-x.height/2, 0))
    # # scene.add(x)

        
    # scene.zoom_out(True, scene.camera.frame_center, scene.camera.frame_width*2)
    # scene.wait(3)

    # scene.changeTreeLayout(layout=TreeLayout.H_V, isAnimation=True)
    # scene.changeRootPackingAndSorting(isAnimation=True, rootSorting=RootSorting.Heigth_Width, rootPacking=RootPacking.Binary_Tree_Packing)
    
    # scene.zoom_out(True, scene.camera.frame_center, scene.camera.frame_width*1.5)
    # scene.wait(3)

    scene.render()
    print("--- %s seconds ---" % (time.time() - start_time))
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()