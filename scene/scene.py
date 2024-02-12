from manim import *

class MobjectPlacement(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nodes = []  # List to keep track of nodes
        self.initial_position = LEFT * 4  # Starting position for the first circle
        self.shift_amount = RIGHT * 2  # Distance to shift nodes to the right

    def add_circle(self):
        # Create a new circle
        new_circle = Circle(radius=1, color=BLUE)
        # Position the new circle at the initial position
        new_circle.move_to(self.initial_position)

        # Shift existing nodes to the right
        for circle in self.nodes:
            circle.animate.move_to()
        
        # Add the new circle to the scene and to the nodes list
        self.play(Create(new_circle))
        self.nodes.append(new_circle)

    def construct(self):
        return