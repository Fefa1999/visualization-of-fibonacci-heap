from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
import random

import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True
config.quality = "high_quality"

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = True
    heap.showExplanatoryText = False
    
    #DO THINGS TO HEAP TO SHOW IN VIDEO FILE 
    for i in range(10):
        heap.insert(i)

    #heap.showExplanatoryText = True
    #heap.isAnimation = True
    heap.extract_min()
    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()