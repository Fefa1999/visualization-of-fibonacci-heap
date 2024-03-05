from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
import random

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
    heap.concurrent_consolidate = False
    
    #SETUP STARTING POINT
    for i in range(550):
        heap.insert(random.randint(0, 500))
        #heap.insert(i)

    #ANIMATIONS
    heap.extract_min()
    heap.isAnimation = True
    heap.insert(1)

    scene.wait()
    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()