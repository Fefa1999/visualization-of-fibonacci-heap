from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *
import random


import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True
config.quality = "low_quality"
#config.quality = "medium_quality"
#config.quality = "high_quality"
#config.quality = "production_quality"
#config.quality = fourk_quality
#config.renderer = "opengl"


def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = True
    for i in range(36):
        heap.insert(i)

    heap.isAnimation = True
    heap.extract_min()
    heap.extract_min()
    heap.extract_min()
    heap.extract_min()
    heap.extract_min()
    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()