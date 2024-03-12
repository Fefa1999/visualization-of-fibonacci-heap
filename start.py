from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from manim_heap import IntroScene
from manim_heap_withoutOGL import HeapScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config
import sys
import time

config.disable_caching = True
config.disable_caching_warning = True
config.quality = "high_quality"
#config.renderer = "opengl"

def run(args):
    start_time = time.time()
    #nodes_to_insert = int(args[1])
    heap = FibonacciHeap()
    if 1 == 1:
        config.renderer = "opengl"
        scene = IntroScene()
    else:
        scene = HeapScene()
    
    heap.scene = scene
    
    for i in range(20):
        print(i)
        heap.insert(i)

    heap.extract_min()
    #heap.insert(0)

    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)
    print("Rendering took", time.time()-start_time)
run(sys.argv)