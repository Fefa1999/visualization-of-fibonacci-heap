from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config

import time

config.disable_caching = True
config.disable_caching_warning = True
config.quality = "low_quality"
#config.renderer = "opengl"

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = False
    
    #DO THINGS TO HEAP TO SHOW IN VIDEO FILE 
    for i in range(20):
        heap.insert(i)
    #heap.insert(2)
    heap.isAnimation = True
    heap.extract_min()
    for i in range(20):
        heap.insert(i)
    heap.extract_min()

    heap.insert(100)

    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()