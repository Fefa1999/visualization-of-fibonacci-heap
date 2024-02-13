from manim import *
from manim.typing import Point3D
from manim.typing import Vector3

class main(Scene):
    def construct(self):
        number_of_nodes = 0
        defaultAddPoint = [-1*((frame.frame_width/2)-0.4),frame.frame_height/2-0.4, 0]
        #self.add(Dot(defaultAddPoint,radius=0.2))
        root = VGroup()

        number_of_nodes+=1
        a = insertDot(self, root, defaultAddPoint, 1, False, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        b = insertDot(self, root, defaultAddPoint, 2, False, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        insertDot(self, root, defaultAddPoint, 3, False, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        c = insertDot(self, root, defaultAddPoint, 4, False, number_of_nodes)
        number_of_nodes+=1
        e = insertDot(self, root, defaultAddPoint, 9, False, number_of_nodes)
        #self.wait(5)
       
        createChild(self, a, b, False)
        root.remove(b)
        insertDot(self, root, defaultAddPoint, 6, False, number_of_nodes)
        createChild(self, a, c, False)
        root.remove(c)
        insertDot(self, root, defaultAddPoint, 7, False, number_of_nodes)
        createChild(self, b, e, False)
        root.remove(e)
        

        d = insertDot(self, root, defaultAddPoint, 5, False, number_of_nodes)
        createChild(self, b, d, False)
        root.remove(d)
        
        f = insertDot(self, root, defaultAddPoint, 10, False, number_of_nodes)
        createChild(self, a, f, False)
        root.remove(f)

        insertDot(self, root, defaultAddPoint, 8, True, number_of_nodes)
        self.wait(10)

#New dot class. A manim dot with children.
class newDot(Dot):
    def __init__(self, id: int, *args, **kwargs):
        self.id = id
        super().__init__(*args, **kwargs)
        self.children = VGroup()
        self.parrent = Mobject()

def arrange_where_buffer_is_subtree_width(
    self,
    direction: Vector3 = RIGHT,
    center: bool = True,
    **kwargs,
):
    for m1, m2 in zip(self.submobjects, self.submobjects[1:]):
        m2.next_to(m1, direction, (m2.children.width + m1.radius*2), **kwargs)
    if center:
        self.center()
    return self

VGroup.arrange_where_buffer_is_subtree_width = arrange_where_buffer_is_subtree_width


#Creates a dot with a location, and return it withour adding it to scene.
def createDot(point: Point3D, number: int, id: int):
    blue_dot = newDot(id, point, radius=0.2, color=BLUE) #TODO add custome radius - was 0.2
    dot_label = Text(str(number)).next_to(blue_dot, 0).set_z_index(1) #TODO add custome scaler for text size
    dot_label.add_updater(
        lambda mobject: mobject.next_to(blue_dot, 0)
    )
    blue_dot.number = dot_label
    return blue_dot

#Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
def insertDot(slf: Scene, group: VGroup, point: Point3D, number: int, fadeIn: bool, id: int):
    dot = createDot(point, number, id)
    group.add(dot)   #Gets inserted into root vgroup... should it be here?
    if fadeIn:
        slf.play(FadeIn(dot, dot.number))
    else:
        slf.add(dot, dot.number)
    rootDisperse(slf, group, fadeIn) #TODO custom height maybe should it be here 
    return dot

def rootDisperse(slf: Scene, group: VGroup, fadeIn: bool):   #Should move from start point based on radius
    size = len(group.submobjects)+2 #to create free endpoints
    height = (frame.frame_height/2)-1
    width = frame.frame_width
    if fadeIn:
        slf.play(group.animate.arrange(buff=(width/size)).set_y(height))  #TODO:Scale with the size of nodes children tree
    else:
        group.arrange(buff=(width/(len(group.submobjects)+2))).set_y(height)


def createChild(slf: Scene, parrentMojb: newDot, childMojb: newDot, isAnimation: bool):
    parrentMojb.children.add(childMojb)
    pointer = Line(childMojb,parrentMojb)
    pointer.add_updater(
        lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller for width
        )
    childMojb.arrow = pointer
    if isAnimation:
        animateChildren(slf, parrentMojb)
        slf.play(FadeIn(pointer))
    else:
        moveChildren(slf, parrentMojb)
        slf.add(pointer)

def animateChildren(slf: Scene, parrentMojb: newDot): #need to be made into a transform method where it can collect all animation and then move.
    if len(parrentMojb.children)==0:
        return
    slf.play(parrentMojb.children.animate.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
    for n in parrentMojb.children:
        animateChildren(slf, n)
    
def moveChildren(slf: Scene, parrentMojb: newDot):
    if len(parrentMojb.children)==0:
        return
    slf.add(parrentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
    for n in parrentMojb.children:
        moveChildren(slf, n)


