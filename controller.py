from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import *
from manim import config
from manim.utils.file_ops import open_file as open_media_file 
from manim import *

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True

config.quality = "low_quality"
#config.quality = "medium_quality"
#config.quality = "high_quality"
#config.quality = "production_quality"
#config.quality = "fourk_quality"

class Controller():
    def __init__(self):
        self.heap : FibonacciHeap = FibonacciHeap()
        self.scene : FiboScene = FiboScene()
        self.isAnimation : bool = False
        self.showExplanatoryText : bool = False

    def set_show_animations(self, show):
        self.isAnimation = show
    
    def set_show_explanatory_text(self, show):
        self.showExplanatoryText = show

    def insert_node(self, value):
        returned_data = self.heap.insert(value)
        node = returned_data[0]
        update_min = returned_data[1]
        self.scene.insert_dot(node.value, self.isAnimation, node.id)
        if update_min:
            self.scene.set_min(node.id, self.isAnimation)
        return node
    
    def extract_min(self):
        returned_data = self.heap.extract_min()
        self.scene.delete(returned_data[0].id, self.isAnimation)
        for nodes in returned_data[1]:
            self.scene.create_child(nodes[0].id, nodes[1].id, self.isAnimation, self.showExplanatoryText)
        self.scene.set_min(returned_data[2].id, self.isAnimation)
    
    def decrease_value(self, node, new_value):
        returned_data = self.heap.decrease_value(node, new_value)
        if returned_data[0]:
            self.scene.change_key(returned_data[1].id, new_value, self.isAnimation, self.showExplanatoryText)
            for node_info in returned_data[2]:
                if isinstance(node_info, tuple):
                    self.scene.cut(node_info[0].id, self.isAnimation, node_info[1], self.showExplanatoryText)
                else:
                    self.scene.cascading_cut(node_info.id, self.isAnimation, self.showExplanatoryText)
            
            if returned_data[3]:
                self.scene.set_min(node.id, self.isAnimation)

    def change_packing(self, rp: RootPacking = RootPacking.FFDH, rs: RootSorting = RootSorting.Order):
        self.scene.changeRootPackingAndSorting(rp, rs, self.isAnimation)
    
    def export_video(self):
        self.scene.render()
        open_media_file(self.scene.renderer.file_writer.movie_file_path)
