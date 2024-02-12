from manim import *
from manim.typing import Point3D

class main(Scene):
    def construct(self):
        number_of_nodes = 0
        defaultAddPoint = [-1*((frame.frame_width/2)-0.4),frame.frame_height/2-0.4, 0]
        #self.add(Dot(defaultAddPoint,radius=0.2))
        root = VGroup()

        number_of_nodes+=1
        a = insertDot(self, root, defaultAddPoint, 1, True, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        b = insertDot(self, root, defaultAddPoint, 2, True, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        insertDot(self, root, defaultAddPoint, 3, True, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        c = insertDot(self, root, defaultAddPoint, 4, True, number_of_nodes)
        number_of_nodes+=1
        e = insertDot(self, root, defaultAddPoint, 9, True, number_of_nodes)
        #self.wait(5)
       
        createChild(self, a, b, True)
        root.remove(b)
        createChild(self, a, c, True)
        root.remove(c)
        createChild(self, a, e, True)
        root.remove(e)
        

        d = insertDot(self, root, defaultAddPoint, 5, True, number_of_nodes)
        createChild(self, b, d, True)
        root.remove(d)
        insertDot(self, root, defaultAddPoint, 6, True, number_of_nodes)
        insertDot(self, root, defaultAddPoint, 7, True, number_of_nodes)
        insertDot(self, root, defaultAddPoint, 8, True, number_of_nodes)
        self.wait(10)

#New dot class. A manim dot with children.
class newDot(Dot):
    def __init__(self, id: int, *args, **kwargs):
        self.id = id
        super().__init__(*args, **kwargs)
        self.children = VGroup()


#Creates a dot with a location, and return it withour adding it to scene.
def createDot(point: Point3D, number: int, id: int):
    blue_dot = newDot(id, point, radius=0.2, color=BLUE) #TODO add custome radius - was 0.2
    dot_label = Text(str(number)).next_to(blue_dot, 0).set_z_index(1) #TODO add custome scaler for text size
    dot_label.add_updater(
        lambda mobject: mobject.next_to(blue_dot, 0)
    )
    blue_dot.number = dot_label
    print(blue_dot.id)
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
        group.arrange(buff=(width/(len(group.submobjects)+2)))



def createChild(slf: Scene, parrentMojb: newDot, childMojb: newDot, isAnimation: bool):
    parrentMojb.children.add(childMojb)
    pointer = Line(childMojb,parrentMojb)
    pointer.add_updater(
        lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller
        )
    childMojb.arrow = pointer
    
    if isAnimation:
        animateChildren(slf, parrentMojb)
        slf.play(FadeIn(pointer))
    else:
        moveChildren(slf, parrentMojb)
        slf.add(pointer)

def animateChildren(slf: Scene, parrentMojb: newDot):
    if len(parrentMojb.children)==0:
        return
    for n in parrentMojb.children:
        animateChildren(slf, n)
    slf.play(parrentMojb.children.animate.arrange(buff=parrentMojb.radius*4, center= False).set_x(parrentMojb.get_x()).set_y(parrentMojb.get_y()-1))

def moveChildren(slf: Scene, parrentMojb: newDot):
    if len(parrentMojb.children)==0:
        return
    for n in parrentMojb.children:
        moveChildren(slf, n)
    slf.add(parrentMojb.children.arrange(buff=parrentMojb.radius*4, center= False).set_x(parrentMojb.get_x()).set_y(parrentMojb.get_y()-1))
