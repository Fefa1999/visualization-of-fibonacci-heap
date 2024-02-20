from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing import TypedDict

#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER

#New dot class. A manim dot with children.
class newDot(Dot):
    def __init__(self, id: int, *args, **kwargs):
        self.id = id
        super().__init__(*args, **kwargs)
        self.children = VGroup()
        self.widthOfChildren = int()
        self.parrentKey = int()
        self.arrow = Line()
        #self.label = Text()

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        self.root = VGroup().add(newDot(0, color=RED))
        self.nodeDic = dict()
        super().__init__(*args, **kwargs)

def arrange_where_buffer_is_subtree_width(
    self,
    direction: Vector3 = LEFT,
    center: bool = True,
    **kwargs,
):
    for m1, m2 in zip(self.submobjects, self.submobjects[1:]):
        m2.next_to(m1, direction, (m1.widthOfChildren), **kwargs)
    if center:
        self.center()
    return self
VGroup.arrange_where_buffer_is_subtree_width = arrange_where_buffer_is_subtree_width

class main(FiboScene):
    def construct(self):
        number_of_nodes = 0
        defaultAddPoint = [0,1, 0]
        isAnimation = False

        print(self.root)

        number_of_nodes+=1
        a = insertDot(self, defaultAddPoint, 1, isAnimation, number_of_nodes)

        print(self.root)

        number_of_nodes+=1
        b = insertDot(self, defaultAddPoint, 2, isAnimation, number_of_nodes)
        number_of_nodes+=1
        c = insertDot(self, defaultAddPoint, 4, isAnimation, number_of_nodes)
        number_of_nodes+=1
        d = insertDot(self, defaultAddPoint, 5, isAnimation, number_of_nodes)
       
        createChild(self, a.id, b.id, isAnimation)

        createChild(self, c.id, d.id, isAnimation)

        createChild(self, a.id, c.id, isAnimation)

        moveToRoot(self, c.id, isAnimation)

        number_of_nodes+=1
        d = insertDot(self, defaultAddPoint, 6, isAnimation, number_of_nodes)
        createChild(self, c.id, d.id, isAnimation)

        createChild(self, a.id, c.id, isAnimation)

        number_of_nodes+=1
        f = insertDot(self, defaultAddPoint, 7, isAnimation, number_of_nodes)
        createChild(self, a.id, f.id, isAnimation)

        number_of_nodes+=1
        g = insertDot(self, defaultAddPoint, 8, isAnimation, number_of_nodes)
        number_of_nodes+=1
        h = insertDot(self, defaultAddPoint, 9, isAnimation, number_of_nodes)
        createChild(self, g.id, h.id, isAnimation)

        isAnimation = False

        number_of_nodes+=1
        i = insertDot(self, defaultAddPoint, 10, isAnimation, number_of_nodes)
        number_of_nodes+=1
        j = insertDot(self, defaultAddPoint, 11, isAnimation, number_of_nodes)
        createChild(self, i.id, j.id, isAnimation)

        createChild(self, g.id, i.id, isAnimation)

        number_of_nodes+=1
        k = insertDot(self, defaultAddPoint, 12, isAnimation, number_of_nodes)
        createChild(self, g.id, k.id, isAnimation)

        number_of_nodes+=1
        insertDot(self, defaultAddPoint, 13, isAnimation, number_of_nodes)
        delete(self, g.id, isAnimation)


        #HEREH FRIST CHECK
        isAnimation = True
        for x in range(2):
            number_of_nodes+=1
            insertDot(self, defaultAddPoint, 14+x, isAnimation, number_of_nodes)

        delete(self, a.id, isAnimation)
        self.wait(10)

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
def insertDot(slf: FiboScene, point: Point3D, number: int, fadeIn: bool, id: int):
    dot = createDot(point, number, id)
    slf.nodeDic[id] = dot

    slf.root.add(dot)   #Gets inserted into root vgroup... should it be here?
    if fadeIn:
        slf.play(FadeIn(dot, dot.number))
    else:
        slf.add(dot, dot.number)
    
    if len(slf.root) == 1: #First node check
        if fadeIn:
            slf.play(slf.root.animate.center())
            return dot
    
    moveToRootSpot(slf, fadeIn)
    adjust_camera(slf, fadeIn)
    return dot

def moveToRootSpot(slf: FiboScene, fadeIn: bool):
    rootlength = len(slf.root)
    addedDot = slf.root[rootlength-1]
    mostRightDot = slf.root[rootlength-2]
    if isinstance(addedDot, newDot) and isinstance(mostRightDot, newDot):
        if fadeIn:
            slf.play(addedDot.animate.next_to(mostRightDot, buff=2*mostRightDot.radius))
        else:
            addedDot.next_to(mostRightDot, buff=2*mostRightDot.radius)             

def adjust_camera(slf: FiboScene, isAnimation: bool):
    mostLeftNode = get_left_most_dot(slf.root)
    mostRightNode = slf.root[len(slf.root)-1]

    if isinstance(mostLeftNode, newDot) and isinstance(mostRightNode, newDot):
        centerR = mostRightNode.get_center()
        centerL = mostLeftNode.get_center()
        newCenter: Point3D = ((centerR[0]+centerL[0])/2, (centerR[1]+centerL[1])/2, (centerR[2]+centerL[2])/2)

        heigthDif = mostRightNode.get_y()-mostLeftNode.get_y()
        widthDif = mostRightNode.get_x()-mostLeftNode.get_x()

        newWidth = heigthDif/(1080/1920)
        if widthDif > newWidth:
            newWidth = widthDif
        if isAnimation:
            slf.play(
                slf.camera.frame.animate.set_height(newWidth*1.03+10),
                slf.camera.frame.animate.move_to(newCenter)
            )
        else:
            slf.camera.frame.set_height(newWidth*1.03+10),
            slf.camera.frame.move_to(newCenter)

        
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

def createChild(slf: Scene, parrentKey: int, childKey: int, isAnimation: bool):
    rootParrentIndex = getRootKeyIndex(slf.root, parrentKey)
    if not isinstance(rootParrentIndex, int):
        return
    parrentMojb = slf.root[rootParrentIndex]

    rootChildIndex = getRootKeyIndex(slf.root, childKey)
    if not isinstance(rootChildIndex, int):
        return
    childMojb = slf.root[rootChildIndex]

    if isinstance(childMojb, newDot):
        childMojb.parrentKey = parrentKey

    if isinstance(parrentMojb, newDot):
        parrentMojb.children.add(childMojb)

        #creating arrow
        pointer = Line(childMojb,parrentMojb)
        pointer.add_updater(
            lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller for width
            )
        childMojb.arrow = pointer

        slf.root.remove(childMojb)
        childWidth = int() 
        if len(parrentMojb.children) == 1:
            childWidth = 0
        else:
            childWidth = childMojb.widthOfChildren + parrentMojb.radius*2
        parrentMojb.widthOfChildren = parrentMojb.widthOfChildren + childWidth

        if isAnimation:
            vg = animateRoot(slf.root, min(rootParrentIndex,rootChildIndex))
            if isinstance(vg, list):
                slf.play(AnimationGroup(*[MoveToTarget(n) for n in vg], lag_ratio=0), FadeIn(pointer))
            #slf.play(FadeIn(pointer)) #Move it up
        else:
            moveRoot(slf, rootParrentIndex)
            slf.add(pointer)

def animateRoot(root: VGroup, startIndex): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
    def aux (root: VGroup, rootIndex: int, lastDotDestination: newDot):
        if rootIndex == len(root):
            return []

        returnList = list()
        currentDot = root[rootIndex]
        if not isinstance(currentDot, newDot): #will be fixed by new vgroup
            return []
        currentDot.generate_target()
        currentDot.target.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())
        returnList.append(currentDot)
        if isinstance(currentDot.target, newDot):
            ch = animateChildren(currentDot, currentDot.target)
        if isinstance(ch, list):
            returnList.extend(ch)
        
        ac = aux(root, rootIndex+1, currentDot.target)

        returnList.extend(ac)

        return returnList
    
    startDot = newDot(0)
    if startIndex != 1: #VGroups first index of subobjects is at 1
        startDot = root[startIndex-1]
    
    return aux(root, startIndex, startDot)

def moveRoot(self: FiboScene, rootIndexOfNewParrent: int):
    if rootIndexOfNewParrent == 0:
        rootDot = self.root[rootIndexOfNewParrent]
        moveChildren(self, rootDot)

    
    def aux (root: VGroup, rootIndex: int, lastDotDestination: newDot):
        if rootIndex == len(root):
            return []
        
        currentDot = root[rootIndex]
        if not isinstance(currentDot, newDot): #will be fixed by new vgroup
            return []
        currentDot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())

        moveChildren(self, currentDot)
        
        aux(root, rootIndex+1, currentDot)

    (aux(self.root, 1, self.root[0]))

def animateChildren(parrentMojb: newDot, parrentTarget: newDot): #need to be made into a transform method where it can collect all animation and then move.
    if len(parrentMojb.children)==0:
        return
    VGroup_list = list()
    parrentMojb.children.generate_target()
    parrentMojb.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentTarget.get_y()-1).align_to(parrentTarget, RIGHT)
    VGroup_list.append(parrentMojb.children)
    for n in range(len(parrentMojb.children)):
        ac = animateChildren(parrentMojb.children[n], parrentMojb.children.target[n])
        if isinstance(ac, list):
            VGroup_list= VGroup_list + ac
    return VGroup_list
    
def moveChildren(slf: FiboScene, parrentMojb: newDot):
    if len(parrentMojb.children)==0:
        return
    slf.add(parrentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
    for n in parrentMojb.children:
        moveChildren(slf, n)

def delete(slf: FiboScene, deleteDotID: int, isAnimation: bool):
    deleteDot = slf.nodeDic.get(deleteDotID)
    index = getRootKeyIndex(slf.root, deleteDotID)

    slf.root.remove(deleteDot)
  
    childrenArrows = []
    if len(deleteDot.children)>0:
        deleteDot.children.submobjects.reverse()
        for n in deleteDot.children.submobjects:
            childrenArrows.append(n.arrow)
            n.parrentKey = None
            slf.root.add(n)

    if isAnimation:
        vg = animateRoot(slf.root, index)
        if isinstance(vg, list):
            slf.play(AnimationGroup(*[MoveToTarget(n) for n in vg], lag_ratio=0), AnimationGroup(*[FadeOut(n) for n in childrenArrows]), FadeOut(deleteDot.number), FadeOut(deleteDot))
    else:
        slf.remove(deleteDot.number)
        slf.remove(deleteDot)
        moveRoot(slf, index-1)
        for n in childrenArrows:
            slf.remove(n)

def moveToRoot(slf: FiboScene, movingDotID: int, isAnimation: bool):
    movingDot = slf.nodeDic.get(movingDotID)
    parrentDot = slf.nodeDic.get(movingDot.parrentKey)

    movingDot.parrentKey = None
    parrentDot.children.remove(movingDot)
    slf.root.add(movingDot)

    if isAnimation:
        vg = animateRoot(slf.root, len(slf.root)-1)
        if isinstance(vg, list):
            slf.play(AnimationGroup(*[MoveToTarget(n) for n in vg], lag_ratio=0), FadeOut(movingDot.arrow))
    else:
        moveRoot(slf, len(slf.root)-1)
        slf.remove(movingDot.arrow)





#NOT USED
def displaceAllNodeToTheRight(root: VGroup, rootIndex: int, displacement: int):
    returnlist = list
    def aux(dot: newDot):
        for n in dot.children:
            returnlist.extend(aux(n))
        dot.generate_target()
        dot.target.set_x(dot.get_x()+displacement)
        returnlist.append(dot)
        return returnlist

    for n in range(len(root)-rootIndex-1):
        currentIndex = rootIndex+1+n
        aux(root[currentIndex])

    return returnlist