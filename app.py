from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *


import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True
config.quality = "low_quality"
#config.quality = "medium_quality"
#config.quality = "high_quality"
#config.quality = "production_quality"
#config.quality = "fourk_quality"
#config.renderer = "opengl"


def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = False
    for i in range(94):
        heap.insert(i)
    #heap.extract_min()
    #heap.decrease_value(20, 0)
    #heap.extract_min()

    heap.isAnimation = True
    heap.extract_min()
    
    #scene.play(scene.camera.frame.animate.set_width(200))
    #heap.extract_min()

    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()