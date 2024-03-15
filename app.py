from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *

import time

config.disable_caching = True
config.disable_caching_warning = True
config.quality = "low_quality"
#config.quality = "high_quality"
#config.renderer = "opengl"

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = True

    heap.insert(10)
    for i in range(8):
        heap.insert(i)
    
    heap.isAnimation = True
    heap.extract_min()
    heap.extract_min()
    # heap.isAnimation = False
    for i in range(32):
        heap.insert(i+130)
    # heap.isAnimation = True
    heap.extract_min()
    scene.wait(10)
    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()