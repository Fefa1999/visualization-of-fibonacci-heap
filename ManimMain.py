from manim import *

class main(Scene):
    def construct(self):

        dot = createDot(self)
        createChild(self, dot)

        
        return


def createDot(slf: Scene): #need to be given self. returns dot
    blue_dot = Dot(color=BLUE)
    dot_label = Text("N").next_to(blue_dot, 0)
    dot_label.add_updater(
        lambda mobject: mobject.next_to(blue_dot, 0)
    )
    slf.add(blue_dot, dot_label)
    blue_dot.number = dot_label
    return blue_dot

def createChild(slf: Scene,parrentMojb: Mobject):
    child = createDot(slf) 
    child.move_to(parrentMojb.get_center() + DOWN)
    pointer = Arrow(child, parrentMojb)
    pointer.add_updater( # place arrow left of dot
        lambda mob: mob.next_to(parrentMojb, child)
    )
    slf.add(child, pointer)
    child.arrow = pointer
    return child

def scaler(dt): #scales depending on number of mobjects
    for mob in self.mobjects:
        mob.set(width=2/(self.mobjects.size/2))
    self.add_updater(scene_scaler)

def ValueTracker():
    line = NumberLine(x_range=[-10, 10])
    position = ValueTracker(0)
    pointer = Vector(DOWN)
    pointer.add_updater(
        lambda mob: mob.next_to(
            line.number_to_point(position.get_value()), UP
        )
    )
    pointer.update()
    self.add(line, pointer)
    self.wait()
    self.play(position.animate.set_value(4))
    self.play(position.animate.set_value(-2))