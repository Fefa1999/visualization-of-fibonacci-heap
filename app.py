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
    for i in range(82):
        heap.insert(i)
    heap.isAnimation = True 
    heap.extract_min()
    heap.extract_min()
    heap.extract_min()
    for i in range(15):
        heap.insert(i+82)
    heap.extract_min()
    heap.decrease_value(83, -1)
    heap.decrease_value(84, -2)
    heap.extract_min()
    # heap.isAnimation = True
    # Wanted_height = 7
    # n = 500
    # indexTodecrease = 1
    # heap.insert(0)
    # for i in range(Wanted_height):
    #     heap.insert(n)
    #     heap.insert(n-1)
    #     n-=2
    #     heap.extract_min()
    #     heap.decrease_value(indexTodecrease, 0)
    #     indexTodecrease += 2

    scene.render()
    print("--- %s seconds ---" % (time.time() - start_time))
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()