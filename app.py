from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import FiboScene
from Manim5_openGL import Glscene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
import random
import time

config.disable_caching = True
config.disable_caching_warning = True
config.quality = "low_quality"
openGL = True

def run():
    #SETUP 
    start_time = time.time()
    heap = FibonacciHeap()
    scene = FiboScene()
    if openGL:
        config.renderer = "opengl"
        scene = Glscene()
    
    heap.scene = scene

    #Set animation 
    heap.isAnimation = False
    heap.concurrent_consolidate = True
    
    #SETUP STARTING POINT
    for i in range(40):
        heap.insert(random.randint(0, 500))

    #ANIMATIONS
    heap.isAnimation = True
    heap.extract_min()
    heap.insert(100000)

    scene.wait()
    scene.render()

    print("--- %s seconds ---" % (time.time() - start_time))

    open_media_file(scene.renderer.file_writer.movie_file_path)
run()