from manim import *
from manim.opengl import *

class IntroScene(Scene):
    i_p = []
    root = []
    min_node = None
    start_frame_width = None
    start_frame_height = None
    start_frame_multiplier = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i_p = [self.camera.get_center()[0], self.camera.get_center()[1]+(self.camera.get_top()[1]/2), self.camera.get_center()[2]]
        self.start_frame_width = self.camera.get_width()
        self.start_frame_height = self.camera.get_height()
    
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
        #self.play(FadeIn(dot), FadeIn(dot.label))
        self.add(dot, dot.label)
        self.root.append(dot)
        self.move_to_spot_in_root(dot)
        self.adjust_camera()
        
    def move_to_spot_in_root(self, dot):
        if len(self.root) == 1:
            #self.play(dot.animate.move_to([self.i_p[0], self.i_p[1]-1, self.i_p[2]]))
            #self.play(dot.label.animate.move_to(dot.get_center()))
            dot.move_to([self.i_p[0], self.i_p[1]-1, self.i_p[2]])
            dot.label.move_to(dot.get_center())
        else:
            x = self.root[len(self.root)-2].get_x()+1
            y = self.root[len(self.root)-2].get_y()
            #self.play(dot.animate.move_to([x, y, 0]))
            #self.play(dot.label.animate.move_to(dot.get_center()))
            dot.move_to([x, y, 0])
            dot.label.move_to(dot.get_center())

    def update_min_node(self, id):
        prev_min = self.min_node
        for node in self.root:
            if node.id == id:
                self.min_node = node
                break
        if prev_min != None:
            prev_min.color = BLUE
        self.min_node.color = RED
        
    def delete_node(self, id):
        dot = next((dot for dot in self.root if dot.id == id), None)
        index = self.root.index(dot)
        self.root.remove(dot)
        #self.play(FadeOut(dot, dot.label))
        self.remove(dot, dot.label)
        #animations = []
        for i in range(index, len(self.root)):
            dot_to_move = self.root[i]
            new_position = [dot_to_move.get_x()-1, dot_to_move.get_y(), 0]
            dot_to_move.move_to(new_position)
            dot_to_move.label.move_to(new_position)
            #animations.append(dot_to_move.animate.move_to(new_position))
        #self.play(*animations)

    #UPDATE WHEN CHILDREN ARE IMPLEMENTED
    def get_leftmost_dot(self):
        dot = self.root[0]
        return dot

    #CORRECT
    def get_rightmost_dot(self):
        dot = self.root[len(self.root)-1]
        return dot

    def adjust_camera(self):
        left_x = self.get_leftmost_dot().get_center()[0]
        right_x = self.get_rightmost_dot().get_center()[0]
        c_x = self.camera.get_center()[0]
        current_width = (right_x - left_x)
        
        #Zoom out
        if (right_x+1.4) > self.camera.get_right()[0]:
            self.camera.set_width((self.camera.get_width() + self.start_frame_width))

        #zoom in 
        if current_width+1.4 < (self.camera.get_width() - self.start_frame_width):
            new_width = self.camera.get_width()
            while True:
                new_width -= self.start_frame_width
                if  new_width - self.start_frame_width < self.camera.get_width():
                    break
            self.camera.set_width(new_width)
        
        #Centralize camera
        if current_width/2 != c_x:
            self.camera.set_x(current_width/2)
            self.i_p[0] = current_width/2

    def link_nodes(self, parent_id, child_id):
        parent = next((dot for dot in self.root if dot.id == parent_id), None)
        child  = next((dot for dot in self.root if dot.id == child_id), None)
        parent.children.add(child)
        child.parent = parent
        if len(parent.children) == 1:
            self.play(child.animate.move_to([parent.get_x(), parent.get_y()-1, 0]))
        elif len(parent.children) == 2 or len(parent.children) == 3:
            self.play(child.animate.move_to([parent.get_x()-(len(parent.children)-1), parent.get_y()-1, 0]))
            self.play(child.children.animate.move_to([child.get_x()-(len(child.children)-1), child.get_y()-1, 0]))
        else:
            self.play(child.animate.move_to([parent.get_x()-len(parent.children)*2, parent.get_y()-1, 0]))

    


        
        