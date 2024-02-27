from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim4 import FiboScene
from manim.utils.file_ops import open_file as open_media_file 
from manim import config

config.disable_caching = False
config.disable_caching_warning = True
config.quality = "low_quality"
#config.renderer = "opengl"

def run():
    #SETUP 
    heap = FibonacciHeap()
    scene = FiboScene()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = False
    
    #DO THINGS TO HEAP TO SHOW IN VIDEO FILE 
    for i in range(150):
        heap.insert(i)
    #heap.insert(2)
    #for i in range(8, 22):
        #heap.insert(i)
    #heap.isAnimation = True
    heap.extract_min()
    #heap.extract_min()
    heap.isAnimation = True
    heap.insert(120)
    #heap.extract_min()

    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()