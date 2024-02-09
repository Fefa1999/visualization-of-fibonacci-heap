from FibonacciHeap.FibonacciHeap import FibonacciHeap
from scene.scene import MobjectPlacement
from manim.utils.file_ops import open_file as open_media_file 

def run():
    heap = FibonacciHeap()
    scene = MobjectPlacement()
    scene.test()
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)

    for i in range(4):
        heap.insert(i)

    heap.extract_min()
    heap.printHeap()
run()
