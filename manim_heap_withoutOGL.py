from manim import *

class HeapScene(MovingCameraScene):
    i_p = []
    root = []
    min_node = None
    frame_width = None
    frame_height = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i_p = [self.camera.frame.get_center()[0], self.camera.frame.get_center()[1]+(self.camera.frame.get_top()[1]/2), self.camera.frame.get_center()[2]]
        self.frame_width = self.camera.frame.get_width()
        self.frame_height = self.camera.frame.get_height()
    
    def construct(self):
        self.wait()

    class newDot(Dot):
        def __init__(self, id, number, *args, **kwargs):
            super().__init__(*args, **kwargs)
            dot_label = Text(str(number), font_size=18 - (number/100)).move_to([self.get_center()]).set_z(1)
            dot_label.add_updater(
                lambda mobject: mobject.move_to(self.get_center())
            )
            self.children = VGroup()
            self.parent = None
            self.text = None
            self.id = id
            self.label = dot_label

    def insert_node(self, number, id):
        dot = self.newDot(id, number, self.i_p, radius=0.2, color = BLUE)
        self.play(FadeIn(dot), FadeIn(dot.label))
        self.root.append(dot)
        self.move_to_spot_in_root(dot)
        

    def move_to_spot_in_root(self, dot):
        if len(self.root) == 1:
            self.play(dot.animate.move_to([self.i_p[0], self.i_p[1]-1, self.i_p[2]]))
        else:
            x = self.root[len(self.root)-2].get_x()+1
            y = self.root[len(self.root)-2].get_y()
            self.play(dot.animate.move_to([x, y, 0]))

    def update_min_node(self, id):
        prev_min = self.min_node
        for node in self.root:
            if node.id == id:
                self.min_node = node
                break
        if prev_min != None:
            prev_min.color = BLUE
        self.min_node.color = RED
        
    #UPDATE WHEN CHILDREN ARE IMPLEMENTED
    def get_leftmost_dot(self):
        dot = self.root[0]
        return dot

    #CORRECT
    def get_rightmost_dot(self):
        dot = self.root[len(self.root)-1]
        return dot