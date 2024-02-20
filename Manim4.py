from manim import *
from manim.typing import Point3D
from manim.typing import Vector3

class main(MovingCameraScene):
    defaultAddPoint = [-2,1, 0]
    root = VGroup()
    isAnimation = True
    
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
        direction: Vector3 = LEFT,
        center: bool = True,
        **kwargs,
    ):
        for m1, m2 in zip(self.submobjects, self.submobjects[1:]):
            m2.next_to(m1, direction, (m2.widthOfChildren), **kwargs)
        if center:
            self.center()
        return self

    VGroup.arrange_where_buffer_is_subtree_width = arrange_where_buffer_is_subtree_width

    def getRootKeyIndex(self, root: VGroup, key: int):
        for n in range(len(root)):
            a = root[n]
            if isinstance(a, self.newDot):
                if a.id == key:
                    return n
        return

    #Creates a dot with a location, and return it withour adding it to scene.
    def createDot(self, point: Point3D, number: int, id: int):
        blue_dot = self.newDot(id, point, radius=0.2, color=BLUE) #TODO add custome radius - was 0.2
        dot_label = Text(str(number)).next_to(blue_dot, 0).set_z_index(1) #TODO add custome scaler for text size
        dot_label.add_updater(
            lambda mobject: mobject.next_to(blue_dot, 0)
        )
        blue_dot.number = dot_label
        blue_dot.widthOfChildren = blue_dot.radius*2
        return blue_dot

    #Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
    def insertDot(self, number: int, fadeIn: bool, id: int):
        dot = self.createDot(self.defaultAddPoint, number, id)
        self.root.add(dot)   #Gets inserted into root vgroup... should it be here?
        if fadeIn:
            self.play(FadeIn(dot, dot.number))
        else:
            self.add(dot, dot.number)
        
        if len(self.root) == 1: #First node check
            if fadeIn:
                self.play(self.root.animate.center())
                return dot
        
        self.moveToRootSpot(self.root, fadeIn)
        self.adjust_camera(self.root, fadeIn)
        return dot

    def moveToRootSpot(self: Scene, root: VGroup, fadeIn: bool):
        addedDot = root[len(root)-1]
        mostRightDot = root[len(root)-2]
        if isinstance(addedDot, self.newDot) and isinstance(mostRightDot, self.newDot):
            if fadeIn:
                self.play(addedDot.animate.next_to(mostRightDot, buff=2*mostRightDot.radius))  #TODO:Scale with the size of nodes children tree
            else:
                addedDot.next_to(mostRightDot, buff=2*mostRightDot.radius)

    def adjust_camera(self, root: VGroup, fadeIn: bool):
        mostLeftNode = self.get_left_most_dot(root)
        mostRightNode = root[len(root.submobjects)-1]

        if isinstance(mostLeftNode, self.newDot) and isinstance(mostRightNode, self.newDot):
            centerR = mostRightNode.get_center()
            centerL = mostLeftNode.get_center()
            newCenter: Point3D = ((centerR[0]+centerL[0])/2, (centerR[1]+centerL[1])/2, (centerR[2]+centerL[2])/2)

            heigthDif = mostRightNode.get_y()-mostLeftNode.get_y()
            widthDif = mostRightNode.get_x()-mostLeftNode.get_x()

            newWidth = heigthDif/(1080/1920)
            if widthDif > newWidth:
                newWidth = widthDif
            if fadeIn: 
                self.play(
                    self.camera.frame.animate.set_height(newWidth*1.03+10),
                    self.camera.frame.animate.move_to(newCenter)
                )
            else: 
                self.camera.frame.set_height(newWidth*1.03+10),
                self.camera.frame.move_to(newCenter)

    def get_left_most_dot(self, group: VGroup):
        if len(group) == 0:
            return
        
        def aux(a: self.newDot):
            if len(a.children) > 0:
                return aux(a.children.submobjects[0])
            else:
                return a
        
        biggestTreesRoot = group[0]
        if isinstance(biggestTreesRoot, self.newDot):
            mostLeftNode = aux(biggestTreesRoot)
            return mostLeftNode
        
    def find_tree_width(self, dot: newDot):
        padding = dot.radius*2
        if len(dot.children) < 2: 
            dot.widthOfChildren = padding
            return dot.widthOfChildren
        
        leftMost = self.get_left_most_dot(dot.children)
        if isinstance(leftMost, self.newDot):
            dot.widthOfChildren = dot.get_x()-leftMost.get_x()+padding
            return dot.widthOfChildren
        return

    def createChild(self, parentKey: int, childKey: int, isAnimation: bool):
        rootParentIndex = self.getRootKeyIndex(self.root, parentKey)
        if not isinstance(rootParentIndex, int):
            return
        parentMojb = self.root[rootParentIndex]

        rootChildIndex = self.getRootKeyIndex(self.root, childKey)
        if not isinstance(rootChildIndex, int):
            return
        childMojb = self.root[rootChildIndex]

        if isinstance(parentMojb, self.newDot):
            parentMojb.children.add(childMojb)

            #creating arrow
            pointer = Line(childMojb,parentMojb)
            pointer.add_updater(
                lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parentMojb.get_bottom()) #TODO add custome scaller for width
                )
            childMojb.arrow = pointer

            self.root.remove(childMojb)
            childWidth = int() 
            if len(parentMojb.children) == 1:
                childWidth = 0
            else:
                childWidth = childMojb.widthOfChildren + parentMojb.radius*2
            parentMojb.widthOfChildren = parentMojb.widthOfChildren + childWidth

            if isAnimation:
                vg = self.animateRoot(self.root, rootParentIndex)
                if isinstance(vg, list):
                    self.play(AnimationGroup(*[MoveToTarget(n) for n in vg], lag_ratio=0), FadeIn(pointer))
                self.play(FadeIn(pointer)) #Move it up
            else:
                self.moveRoot(self, self.root, rootParentIndex)
                self.add(pointer)

    def animateRoot(self, root: VGroup, rootIndexOfNewParrent: int): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        returnList = list()

        #If the root node is the first -> no displament of any node nesesary
        if rootIndexOfNewParrent == 0:
            rootDot = root[rootIndexOfNewParrent]
            ch = self.animateChildren(rootDot, rootDot)
            if isinstance(ch, list):
                returnList.extend(ch)

        
        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return []

            returnList2 = list()
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return []
            currentDot.generate_target()
            currentDot.target.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2)
            returnList2.append(currentDot)
            if isinstance(currentDot.target, self.newDot):
                ch = self.animateChildren(currentDot, currentDot.target)
            if isinstance(ch, list):
                returnList2.extend(ch)
            
            ac = aux(root, rootIndex+1, currentDot.target)

            returnList2.extend(ac)

            return returnList2

        returnList.extend(aux(root, 1, root[0]))
        return returnList

    def moveRoot(self: Scene, root: VGroup, rootIndexOfNewParrent: int):
        if rootIndexOfNewParrent == 0:
            rootDot = root[rootIndexOfNewParrent]
            self.moveChildren(self, rootDot)

        
        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return []
            
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return []
            currentDot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2)

            self.moveChildren(self, currentDot)
            
            aux(root, rootIndex+1, currentDot)

        (aux(root, 1, root[0]))

    def animateChildren(self, parentMojb: newDot, parrentTarget: newDot): #need to be made into a transform method where it can collect all animation and then move.
        if len(parentMojb.children)==0:
            return
        VGroup_list = list()
        parentMojb.children.generate_target()
        parentMojb.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentTarget.get_y()-1).align_to(parrentTarget, RIGHT)
        VGroup_list.append(parentMojb.children)
        for n in range(len(parentMojb.children)):
            ac = self.animateChildren(parentMojb.children[n], parentMojb.children.target[n])
            if isinstance(ac, list):
                VGroup_list= VGroup_list + ac
        return VGroup_list
        
    def moveChildren(self: Scene, parentMojb: newDot):
        if len(parentMojb.children)==0:
            return
        self.add(parentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parentMojb.get_y()-1).align_to(parentMojb, RIGHT))
        for n in parentMojb.children:
            self.moveChildren(self, n)