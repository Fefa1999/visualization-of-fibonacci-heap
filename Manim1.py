from manim import *
from manim.typing import Point3D

class main(Scene):
    def construct(self):
        defaultAddPoint = [-1*((frame.frame_width/2)-0.4),frame.frame_height/2-0.4, 0]
        #self.add(Dot(defaultAddPoint,radius=0.2))
        root = VGroup()
        
        a = insertDot(self, root, defaultAddPoint, 1, True)
        b = insertDot(self, root, defaultAddPoint, 2, True)
        createChild(self, a, b, True)
        root.remove(root[len(root)-1])
        self.wait()
        c = insertDot(self, root, defaultAddPoint, 3, True)
        d = insertDot(self, root, defaultAddPoint, 4, True)
        createChild(self, c, d, True)
        root.remove(root[len(root)-1])
        createChild(self, a, c, True)
        root.remove(root[len(root)-1])
        self.wait()


        """insertDot(self, root, defaultAddPoint, 1, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 2, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 3, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 4, True)
        self.wait()
        x = insertDot(self, root, defaultAddPoint, 5, True)
        self.wait()
        createChild(self, root[0], root[len(root)-1], True)
        root.remove(root[len(root)-1])
        insertDot(self, root, defaultAddPoint, 6, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 7, True)
        self.wait()
        createChild(self, root[0], root[len(root)-1], True)
        root.remove(root[len(root)-1])
        insertDot(self, root, defaultAddPoint, 8, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 9, True)
        self.wait()
        createChild(self, root[0], root[len(root)-1], True)
        root.remove(root[len(root)-1])
        insertDot(self, root, defaultAddPoint, 10, True)
        self.wait()
        insertDot(self, root, defaultAddPoint, 11, True)
        self.wait()
        self.wait(5)"""
        return
    
#New dot class. A manim dot with children.
class newDot(Dot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = []
    def nadd(self, mobj: VMobject):
        self.children.append(mobj)

def createDot(point: Point3D, number: int):
    blue_dot = newDot(point, radius=0.2, color=BLUE) #TODO add custome radius - was 0.2
    dot_label = Text(str(number)).next_to(blue_dot, 0) #TODO add custome scaler for text size
    dot_label.add_updater(
        lambda mobject: mobject.next_to(blue_dot, 0)
    )
    blue_dot.number = dot_label
    return blue_dot

def insertDot(slf: Scene, group: VGroup, point: Point3D, number: int, fadeIn: bool):
    dot = createDot(point, number)
    group.add(dot)   #Gets inserted into root vgroup... should it be here?
    if fadeIn:
        slf.play(FadeIn(dot, dot.number))
    else:
        slf.add(dot, dot.number)
    rootDisperse(slf, group, fadeIn) #TODO custom height maybe should it be here 
    return dot

def rootDisperse(slf: Scene, group: VGroup, fadeIn: bool):   #Should move move from start point based on radius
    counter = 1
    size = len(group)+2 #to create free endpoints
    height = (frame.frame_height/2)-1
    width = frame.frame_width
    spacingArray = np.linspace(-1*width/2, width/2, size)
    if fadeIn:
        list = []
        for d in group: 
            list.append(d.animate.move_to([spacingArray[counter], height, 0], aligned_edge=UP))
            counter += 1
        slf.play(*list)
    else:
        for d in group: 
            d.move_to([spacingArray[counter], height,0])
            counter += 1

def createChild(slf: Scene, parrentMojb: newDot, childMojb: newDot, isAnimation: bool):
    parrentMojb.nadd(childMojb)
    group = parrentMojb.children
    pointer = Line(childMojb,parrentMojb)
    pointer.add_updater(
        lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller
        )
    childMojb.arrow = pointer

    counter = 1
    size = len(group)+2 #to create free endpoints
    print(size)
    x = parrentMojb.get_x()
    y = parrentMojb.get_y()
    width = 4 #TODO custome width
    spacingArray = np.linspace(-1*width/2, width/2, size)
    if isAnimation:
        list = []
        for d in group: 
            d.clear_updaters()
            list.append(d.animate.move_to([spacingArray[counter]+x, y-1, 0]))
            """ 
            #DOESNT WORK sad smiley
            d.add_updater(
                lambda mobject: d.move_to([spacingArray[counter]+parrentMojb.get_x(), parrentMojb.get_y()-1, 0])
                )
            """
            #TODO add custome displacement
            counter += 1
        slf.play(*list)
    else:
        for d in group: 
            d.move_to([spacingArray[counter]+x, y-1,0])
            counter += 1

    if isAnimation:
        slf.play(FadeIn(pointer))
    else:
        slf.add(pointer)
    