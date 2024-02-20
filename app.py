from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim4 import main
from manim.utils.file_ops import open_file as open_media_file 

def run():
    #SETUP 
    heap = FibonacciHeap()
    scene = main()
    heap.scene = scene

    #Set animation 
    heap.isAnimation = True
    
    #DO THINGS TO HEAP TO SHOW IN VIDEO FILE 
    for i in range(10):
        heap.insert(i)

    #heap.isAnimation = True

    #heap.extract_min()

    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()
