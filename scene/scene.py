from manim import *
from Fibonacci_heap.FibonacciHeap import FibonacciHeap
import math

class FibonacciHeapVisualization(MovingCameraScene):
    scaler = 1
    min_width_right = None
    center = [6.5, -3, 0]
    class CustomVGroup(VGroup):
        def __init__(self, *mobjects, degree="", **kwargs):
            super().__init__(*mobjects, **kwargs)
            self.degree = degree
    
    def setup(self):
        self.all_nodes = {}
        self.root_list_nodes = {}  # List to keep track of the nodes in the root list
        self.next_node_position = [0, 0, 0]  # Position for the next node to be placed before moving
        self.root_group = VGroup()
        self.play(
            self.camera.frame.animate.move_to(self.center)
        )

    def create_fibonacci_heap_node(self, fib_node):
        """Creates a visual representation of a Fibonacci heap node."""
        node = Circle(radius=0.25, color=BLUE)
        node_text = Text(str(fib_node.value), font_size=24).move_to(node.get_center())
        node_group = self.CustomVGroup(node, node_text, degree = fib_node.degree)
        node_group.name = fib_node.id
        self.all_nodes[node_group.name] = node_group

    def insert_into_root_list(self, node_group_name):
        """Inserts a node into the root list and animates the process."""
        if len(self.root_list_nodes) != 0:
            for key in self.root_list_nodes:
                node = self.root_list_nodes[key]
                np = [node.get_center()[0]+1.5, node.get_center()[1], node.get_center()[2]]
                node.move_to(np)
        
        # Set initial position at the top center
        self.all_nodes.get(node_group_name).move_to(self.next_node_position)
        self.play(FadeIn( self.all_nodes.get(node_group_name)))

        # Insert the new node at the beginning of the root list
        self.root_list_nodes[node_group_name] = self.all_nodes.get(node_group_name)

    def remove_from_root_list(self, node_group_name):
        node = self.root_list_nodes.pop(node_group_name)
        x_center = node.get_center()[0]
        self.play(FadeOut(node))
        if len(self.root_list_nodes) != 0:
            for key in self.root_list_nodes:
                node = self.root_list_nodes[key]
                if node.get_center()[0] > x_center:
                    np = [node.get_center()[0]-1.5, node.get_center()[1], node.get_center()[2]]
                    node.move_to(np)

    def link_nodes(self, node_group_name_child, node_group_name_parent):
        
        return


    # def adjust_camera(self):
    #     modifier = (len(self.root_list_nodes) / 8 ) + 1
    #     self.play(
    #         self.camera.frame.animate.scale(self.scaler+1).move_to([6.5*modifier, (3*modifier)*-1, 0])
    #     )
    #     self.scaler = self.scaler/2
    #     return

    def construct(self):
        self.setup()
