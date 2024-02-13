from manim import *
from manim.typing import Point3D
from manim.typing import Vector3

class main(MovingCameraScene):
    def construct(self):
        number_of_nodes = 0
        defaultAddPoint = [-2,1, 0]
        root = VGroup()
        isAnimation = False

        number_of_nodes+=1
        a = insertDot(self, root, defaultAddPoint, 1, isAnimation, number_of_nodes)
        number_of_nodes+=1
        b = insertDot(self, root, defaultAddPoint, 2, isAnimation, number_of_nodes)
        #self.wait()
        number_of_nodes+=1
        c = insertDot(self, root, defaultAddPoint, 4, isAnimation, number_of_nodes)
        number_of_nodes+=1
        e = insertDot(self, root, defaultAddPoint, 5, isAnimation, number_of_nodes)
        #self.wait(5)
       
        createChild(self, root, a, b, isAnimation)

        createChild(self, root, a, c, isAnimation)

        createChild(self, root, b, e, isAnimation)

        number_of_nodes+=1
        d = insertDot(self, root, defaultAddPoint, 6, isAnimation, number_of_nodes)
        createChild(self, root, b, d, isAnimation)

        number_of_nodes+=1
        f = insertDot(self, root, defaultAddPoint, 7, isAnimation, number_of_nodes)
        createChild(self, root, a, f, isAnimation)

        number_of_nodes+=1
        g = insertDot(self, root, defaultAddPoint, 8, isAnimation, number_of_nodes)
        number_of_nodes+=1
        h = insertDot(self, root, defaultAddPoint, 9, isAnimation, number_of_nodes)
        createChild(self, root, g, h, isAnimation)

        isAnimation = True

        number_of_nodes+=1
        i = insertDot(self, root, defaultAddPoint, 10, isAnimation, number_of_nodes)
        number_of_nodes+=1
        j = insertDot(self, root, defaultAddPoint, 11, isAnimation, number_of_nodes)
        createChild(self, root, i, j, isAnimation)

        createChild(self, root, g, i, isAnimation)

        number_of_nodes+=1
        k = insertDot(self, root, defaultAddPoint, 12, isAnimation, number_of_nodes)
        createChild(self, root, g, k, isAnimation)

        isAnimation = False
        for x in range(5):
            number_of_nodes+=1
            insertDot(self, root, defaultAddPoint, 13+x, isAnimation, number_of_nodes)
        self.wait(10)

#New dot class. A manim dot with children.
class newDot(Dot):
    def __init__(self, id: int, *args, **kwargs):
        self.id = id
        super().__init__(*args, **kwargs)
        self.children = VGroup()
        self.widthOfChildren = int()
        #self.parrent = Mobject()

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

def getRootKeyIndex(root: VGroup, key: int):
    for n in range(len(root)):
        a = root[n]
        if isinstance(a, newDot):
            if a.id == key:
                return n
    return

#Creates a dot with a location, and return it withour adding it to scene.
def createDot(point: Point3D, number: int, id: int):
    blue_dot = newDot(id, point, radius=0.2, color=BLUE) #TODO add custome radius - was 0.2
    dot_label = Text(str(number)).next_to(blue_dot, 0).set_z_index(1) #TODO add custome scaler for text size
    dot_label.add_updater(
        lambda mobject: mobject.next_to(blue_dot, 0)
    )
    blue_dot.number = dot_label
    blue_dot.widthOfChildren = blue_dot.radius*2
    return blue_dot

#Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
def insertDot(slf: Scene, group: VGroup, point: Point3D, number: int, fadeIn: bool, id: int):
    dot = createDot(point, number, id)
    group.add(dot)   #Gets inserted into root vgroup... should it be here?
    if fadeIn:
        slf.play(FadeIn(dot, dot.number))
    else:
        slf.add(dot, dot.number)
    
    if len(group) == 1: #First node check
        if fadeIn:
            slf.play(group.animate.center())
            return dot
    
    moveToRootSpot(slf, group, fadeIn)
    adjust_camera(slf, group)
    return dot

def moveToRootSpot(slf: Scene, root: VGroup, fadeIn: bool):
    addedDot = root[len(root)-1]
    mostRightDot = root[len(root)-2]
    if isinstance(addedDot, newDot) and isinstance(mostRightDot, newDot):
        if fadeIn:
            slf.play(addedDot.animate.next_to(mostRightDot, buff=2*mostRightDot.radius))  #TODO:Scale with the size of nodes children tree
        else:
            addedDot.next_to(mostRightDot, buff=2*mostRightDot.radius)


            
                

def adjust_camera(self, root: VGroup):
    mostLeftNode = get_left_most_dot(root)
    mostRightNode = root[len(root.submobjects)-1]

    if isinstance(mostLeftNode, newDot) and isinstance(mostRightNode, newDot):
        centerR = mostRightNode.get_center()
        centerL = mostLeftNode.get_center()
        newCenter: Point3D = ((centerR[0]+centerL[0])/2, (centerR[1]+centerL[1])/2, (centerR[2]+centerL[2])/2)

        heigthDif = mostRightNode.get_y()-mostLeftNode.get_y()
        widthDif = mostRightNode.get_x()-mostLeftNode.get_x()

        newWidth = heigthDif/(1080/1920)
        if widthDif > newWidth:
            newWidth = widthDif
        self.play(
            self.camera.frame.animate.set_height(newWidth*1.03+10),
            self.camera.frame.animate.move_to(newCenter)
        )
        
def get_left_most_dot(group: VGroup):
    if len(group) == 0:
        return
    
    def aux(a:  newDot):
        if len(a.children) > 0:
            return aux(a.children.submobjects[0])
        else:
            return a
    
    biggestTreesRoot = group[0]
    if isinstance(biggestTreesRoot, newDot):
        mostLeftNode = aux(biggestTreesRoot)
        return mostLeftNode
    
def find_tree_width(dot: newDot):
    padding = dot.radius*2
    if len(dot.children) < 2: 
        dot.widthOfChildren = padding
        return dot.widthOfChildren
    
    leftMost = get_left_most_dot(dot.children)
    if isinstance(leftMost, newDot):
        dot.widthOfChildren = dot.get_x()-leftMost.get_x()+padding
        return dot.widthOfChildren
    return



def createChild(slf: Scene, root: VGroup, parrentKey: int, childMojb: newDot, isAnimation: bool):
    parrentMojb = root[getRootKeyIndex(parrentKey)]
    if isinstance(parrentMojb, newDot):
        parrentMojb.children.add(childMojb)

        #creating arrow
        pointer = Line(childMojb,parrentMojb)
        pointer.add_updater(
            lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller for width
            )
        childMojb.arrow = pointer

        root.remove(childMojb)
        parrentMojb.widthOfChildren = parrentMojb.widthOfChildren + childMojb.widthOfChildren + parrentMojb.radius*2 #added padding

        if isAnimation:
            
            vg = animateChildren(slf, parrentMojb, parrentMojb)
            if isinstance(vg, list):
                slf.play(AnimationGroup(*[MoveToTarget(n) for n in vg], lag_ratio=0), FadeIn(pointer))
            slf.play(FadeIn(pointer)) #Move it up
        else:
            moveChildren(slf, parrentMojb)
            slf.add(pointer)

def animateRoot(root: VGroup, rootIndexOfNewParrent: int):
    if len(root)<2:
        return
    returnList = list()
    for n in range(len(root)-rootIndexOfNewParrent):
        rootDot = root[n+rootIndexOfNewParrent]
        if isinstance(rootDot, newDot):
            rootDot.generate_target()
            rootDot.target.set_x(root[n+rootIndexOfNewParrent-1].get_x()+rootDot.widthOfChildren+rootDot.radius*2)
            returnList.append(rootDot)
        #Call animate children 
    return returnList
    #self.play(AnimationGroup(*[MoveToTarget(n) for n in returnList], lag_ratio=0))

def moveRoot(self: Scene, root: VGroup, rootIndexOfNewParrent: int):
    if len(root)<2:
        return
    returnList = list()
    for n in range(len(root)-1):
        rootDot = root[n+1]
        if isinstance(rootDot, newDot):
            mostLeftInTree: newDot
            widthDif: float
            if len(rootDot.children)>0:
                mostLeftInTree = get_left_most_dot(rootDot.children)
                widthDif = rootDot.get_x()-mostLeftInTree.get_x()
            else:
                mostLeftInTree = rootDot
                widthDif = 0
       
            rootDot.next_to(root[0], buff=(widthDif+mostLeftInTree.radius*2))
    
    if isAnimation:
        self.play(AnimationGroup(*[MoveToTarget(n) for n in returnList], lag_ratio=0))

def animateChildren(parrentMojb: newDot, parrentTarget: newDot): #need to be made into a transform method where it can collect all animation and then move.
    if len(parrentMojb.children)==0:
        return
    VGroup_list = list()
    parrentMojb.children.generate_target()
    parrentMojb.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentTarget.get_y()-1).align_to(parrentTarget, RIGHT)
    VGroup_list.append(parrentMojb.children)
    for n in range(len(parrentMojb.children.submobjects)):
        ac = animateChildren(parrentMojb.children.submobjects[n], parrentMojb.children.target.submobjects[n])
        if isinstance(ac, list):
            VGroup_list= VGroup_list + ac
    return VGroup_list
    
def moveChildren(slf: Scene, parrentMojb: newDot):
    if len(parrentMojb.children)==0:
        return
    slf.add(parrentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
    for n in parrentMojb.children:
        moveChildren(slf, n)



