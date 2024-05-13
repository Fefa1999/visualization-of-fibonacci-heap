from Fibonacci_heap.FibonacciHeap import FibonacciHeap
from Manim5 import *
from manim import config
from manim.utils.file_ops import open_file as open_media_file 
from manim import *

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True

config.quality = "low_quality" #(854x480 15FPS)
# config.quality = "medium_quality" #(1280x720 30FPS)
# config.quality = "high_quality" # (1920x1080 60FPS)
# config.quality = "production_quality" # (2560x1440 60FPS)
# config.quality = "fourk_quality" # (3840x2160 60FPS)
# config.pixel_height = 720
# config.pixel_width = 1280
# config.frame_rate = 10
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

    def insert(self, value):
        returned_data = self.heap.insert(value)
        node = returned_data[0]
        update_min = returned_data[1]
        self.scene.insert_dot(node.value, self.isAnimation, node.id)
        if update_min:
            self.scene.set_min(node.id, self.isAnimation)
        return node
    
    def extract_min(self):
        returned_data = self.heap.extract_min()
        if returned_data is not None:
            self.scene.delete(returned_data[0].id, self.isAnimation)
            for nodes in returned_data[1]:
                self.scene.create_child(nodes[0].id, nodes[1].id, self.isAnimation, self.showExplanatoryText)
            if returned_data[2] is not None:
                self.scene.set_min(returned_data[2].id, self.isAnimation)
    
    def decrease_value(self, node, new_value):
        returned_data = self.heap.decrease_value(node, new_value)
        self.scene.change_key(returned_data[0].id, new_value, self.isAnimation, self.showExplanatoryText)
        for node_info in returned_data[1]:
            if isinstance(node_info, tuple):
                self.scene.cut(node_info[0].id, self.isAnimation, node_info[1], self.showExplanatoryText)
            else:
                self.scene.cascading_cut(node_info.id, self.isAnimation, self.showExplanatoryText)
        
        if returned_data[2]:
            self.scene.set_min(node.id, self.isAnimation)

    def delete(self, node):
        self.decrease_value(node, -float('inf'))
        self.extract_min()

    def change_packing_and_sorting(self, packing, sorting):
        self.scene.changeRootPackingAndSorting(RootPacking(packing), RootSorting(sorting), self.isAnimation)
    
    def change_tree_layout(self, layout):
        self.scene.changeTreeLayout(TreeLayout(layout))
    
    def export_video(self):
        # #For adding the bounds off the root packing:
        # x = Rectangle(height=self.scene.bounds[1], width=self.scene.bounds[0])
        # x.move_to((0+x.width/2, 0-x.height/2, 0))
        # self.scene.add(x)
        self.scene.render()
        open_media_file(self.scene.renderer.file_writer.movie_file_path)
