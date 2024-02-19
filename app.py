from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from scene.scene import FibonacciHeapVisualization
from manim.utils.file_ops import open_file as open_media_file 

def run():
    heap = FibonacciHeap()
    scene = FibonacciHeapVisualization()
    scene._setup()
    heap.scene = scene

    #DO THINGS TO HEAP TO SHOW IN VIDEO FILE 
    for i in range(9):
        heap.insert(i)

    heap.extract_min()

    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)
run()
