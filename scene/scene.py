from manim import *
from Fibonacci_heap.FibonacciHeap import FibonacciHeap
import math

class FibonacciHeapVisualization(MovingCameraScene):
    center = [6.5, -3, 0]
    movements = []
    most_left_pos = None


    def _setup(self):
        self.all_nodes = {}
        self.root_list_nodes = {}  # List to keep track of the nodes in the root list
        self.next_node_position = [0, 0, 0]  # Position for the next node to be placed before moving
        self.play(
            self.camera.frame.animate.move_to(self.center)
        )

    def create_fibonacci_heap_node(self, fib_node):
        """Creates a visual representation of a Fibonacci heap node."""
        node = Circle(radius=0.25, color=BLUE)
        node_text = Text(str(fib_node.value), font_size=24).move_to(node.get_center())
        node_group = VGroup(node, node_text)
        node_group.name = fib_node.id
        self.all_nodes[node_group.name] = node_group

    def insert_into_root_list(self, node_group_name):
        if len(self.root_list_nodes) != 0:
            moves = []
            for key in self.root_list_nodes:
                node = self.root_list_nodes[key]
                np = [node.get_center()[0]+1.5, node.get_center()[1], node.get_center()[2]]
                moves.append(node.animate.move_to(np))
            self.play(*moves)
        # Set initial position at the top center
        self.all_nodes.get(node_group_name.id).move_to(self.next_node_position)
        self.play(FadeIn( self.all_nodes.get(node_group_name.id)))

        # Insert the new node at the beginning of the root list
        self.root_list_nodes[node_group_name.id] = self.all_nodes.get(node_group_name.id)

    def link_up(self, child, parent):
        if parent.degree == 1:
            np = [self.all_nodes[parent.id].get_center()[0]-(parent.degree-1), self.all_nodes[parent.id].get_center()[1]-1, self.all_nodes[parent.id].get_center()[2]]
        elif parent.degree == 2:
            np = [self.all_nodes[parent.id].get_center()[0]-(parent.degree-1), self.all_nodes[parent.id].get_center()[1]-1, self.all_nodes[parent.id].get_center()[2]]
        else:
            d = math.pow(2, parent.degree-2)
            np = [self.all_nodes[parent.id].get_center()[0]-d, self.all_nodes[parent.id].get_center()[1]-1, self.all_nodes[parent.id].get_center()[2]]
        self.play(
            self.all_nodes[child.id].animate.move_to(np)
        )
        line = Line(self.all_nodes[parent.id][0].get_edge_center(DOWN), self.all_nodes[child.id][0].get_edge_center(UP))
        self.play(Create(line))
        self.all_nodes[parent.id].add(self.all_nodes[child.id])
        self.all_nodes[parent.id].add(line)
        self.wait()

    def delete_node(self, node):
        node_removed = self.all_nodes.pop(node.id)
        if node.id in self.root_list_nodes:
            node_removed = self.root_list_nodes.pop(node.id)
        self.play(
            FadeOut(node_removed)
        )

    # def adjust_camera(self):
    #     modifier = (len(self.root_list_nodes) / 8 ) + 1
    #     self.play(
    #         self.camera.frame.animate.scale(self.scaler+1).move_to([6.5*modifier, (3*modifier)*-1, 0])
    #     )
    #     self.scaler = self.scaler/2
    #     return