from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing import Self
from typing import TypedDict

#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        self.min_node: self.FiboDot = None
        self.root = list[self.FiboDot]()
        self.mobjsTOmove = list[self.FiboDot]()
        self.nodeDic = dict()
        self.defaultAddPoint = [0,3, 0]
        self.height = 7.993754879000781                                                                                                                                                                                              
        self.width = 14.222222222222221
        self.multp = 0
        super().__init__(*args, **kwargs)

    #New dot class. A manim dot with children. #TODO maybe make all functions such as move_to automatik points to dot
    class FiboDot:
        dot: Dot
        id: int
        parrentKey: int
        children: list[Self]
        widthOfChildren: int
        dot: Dot
        arrow: Line = None
        #numberLabel: Text
        target: Point3D
        def __init__(self, idKey: int):
            self.id = idKey
            self.children = list()
            #self.widthOfChildren = int()
            #self.parrentKey = int()
            #self.arrow = Line()
            #self.numberLabel = Text("")
    

    #RRRR
    def space_list_dots_targets_by_tree_width(self, lst: list[FiboDot], direction: Vector3 = LEFT, **kwargs):
        for m1, m2 in zip(lst, lst[1:]):
            m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren), **kwargs)
        return lst
    #list.arrange_where_buffer_is_subtree_width = arrange_where_buffer_is_subtree_width

    #TODO the isnt this a list method.
    def getRootKeyIndex(self, root: list, key: int):
        for n in range(len(root)):
            a = root[n]
            if a.id == key:
                return n
        return -1

    #Creates a dot with a location, and return it withour adding it to scene.
    def createDot(self, point: Point3D, number: int, id: int):
        fiboDot = self.FiboDot(id)
        fiboDot.dot = Dot(point, radius=0.2, color=BLUE)
        #label = Text(str(number), font_size=18).move_to(fiboDot.dot.get_center()).set_z_index(1) #IS set z index slower?
        # label.add_updater(
        #     lambda mobject: mobject.next_to(fiboDot.dot, 0)
        # )
        # fiboDot.numberLabel = label
        fiboDot.widthOfChildren = fiboDot.dot.radius*2
        return fiboDot

    #Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
    def insertDot(self, number: int, isAnimation: bool, id: int):
        fiboDot = self.createDot(self.defaultAddPoint, number, id)
        self.nodeDic[id] = fiboDot
        self.root.append(fiboDot)

        if isAnimation:
            self.play(FadeIn(fiboDot.dot))#, fiboDot.numberLabel))
        else:
            self.add(fiboDot.dot)#, fiboDot.numberLabel)

        self.moveToRootSpot(isAnimation)
        self.adjust_camera(isAnimation)
        return fiboDot

    def moveToRootSpot(self, isAnimation: bool):
        rootlength = len(self.root)
        addedFiboDot = self.root[rootlength-1]
        addedDot = addedFiboDot.dot
        if rootlength == 1:
            if isAnimation:
                self.play(addedFiboDot.dot.animate.move_to([0, 2, 0]))#, addedFiboDot.numberLabel.animate.move_to([0, 2, 0]))
                return
            else:
                addedFiboDot.dot.move_to([0, 2, 0])
                #addedFiboDot.numberLabel.move_to([0, 2, 0])
                return
        
        mostRightDot = self.root[rootlength-2]
        if isAnimation:
            shiftValue = mostRightDot.dot.get_center()-addedDot.get_center() + RIGHT*addedDot.radius*4
            self.play(addedDot.animate.shift(shiftValue))#,addedFiboDot.numberLabel.animate.shift(shiftValue))
            #self.play(addedFiboDot.dot.animate.next_to(mostRightDot.dot, buff=2*mostRightDot.dot.radius))
        else:
            addedFiboDot.dot.next_to(mostRightDot.dot, buff=2*mostRightDot.dot.radius)
            #addedFiboDot.numberLabel.next_to(addedFiboDot.dot, 0)             

    def adjust_camera(self, isAnimation):
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]

        rightPoint = mostRightNode.dot.get_right()
        leftPoint = mostLeftNode.dot.get_left()

        newWidth = rightPoint[0]-leftPoint[0]
        self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2

        boarderRight = self.camera.frame.get_right()[0]
        boarderLeft = self.camera.frame.get_left()[0]

        if newWidth+4 > (self.camera.frame_width) or boarderLeft > (leftPoint[0]+2) or boarderRight < (rightPoint[0]+2): # +4 is secureing padding
            self.multp = (self.camera.frame_width * 2) / self.width
            newCenter = (((rightPoint[0]+leftPoint[0])/2), (self.multp * 2)*-1, (rightPoint[2]+leftPoint[2])/2)
            if isAnimation:
                self.play(self.camera.frame.animate.set(width=self.camera.frame_width * 2).move_to(newCenter))
            else: 
                self.camera.frame.set(width=self.camera.frame_width * 2).move_to(newCenter)
    
    def get_left_most_dot(self, group: list[FiboDot]):
        if len(group) == 0:
            return
        
        def aux(a: self.FiboDot):
            if len(a.children) > 0:
                return aux(a.children[len(a.children)-1])
            else:
                return a
        
        return aux(group[0])
        
    def find_tree_width(self, dot: FiboDot):
        padding = dot.radius*2
        if len(dot.children) < 2: 
            dot.widthOfChildren = padding
            return dot.widthOfChildren
        
        leftMost = self.get_left_most_dot(dot.children)
        if isinstance(leftMost, self.FiboDot):
            dot.widthOfChildren = dot.get_x()-leftMost.get_x()+padding
            return dot.widthOfChildren
        return

    def createChild(self, parrentKey: int, childKey: int, isAnimation: bool):
        rootParrentIndex = self.getRootKeyIndex(self.root, parrentKey)
        
        if rootParrentIndex<0:
            return
        parrentMojb = self.root[rootParrentIndex]

        rootChildIndex = self.getRootKeyIndex(self.root, childKey)
        if rootChildIndex<0:
            return
        childMojb = self.root[rootChildIndex]
        childMojb.parrentKey = parrentKey
        parrentMojb.children.append(childMojb)

        #creating arrow
        pointer = Line(childMojb.dot,parrentMojb.dot)
        # pointer.add_updater(
        #         lambda mob: mob.put_start_and_end_on(childMojb.dot.get_top(), parrentMojb.dot.get_bottom())
        # )
        childMojb.arrow = pointer

        self.root.remove(childMojb)
        gainedWidth = int() 
        if len(parrentMojb.children) == 1: #child or parrentmobj????
            gainedWidth = 0
        else:
            gainedWidth = childMojb.widthOfChildren + childMojb.dot.radius*2
        parrentMojb.widthOfChildren += gainedWidth

        if isAnimation:
            index = min(rootParrentIndex,rootChildIndex)
            self.animateRoot(self.root, index, self.root[index].dot.get_center())
            lst = list()
            for n in self.mobjsTOmove:
                if n.arrow != None:
                    lst.append(n.arrow.animate.put_start_and_end_on(n.dot.target.get_top(), self.nodeDic[n.parrentKey].dot.target.get_bottom()))
            self.play(AnimationGroup(*[MoveToTarget(n.dot) for n in self.mobjsTOmove], lag_ratio=0), FadeIn(pointer), *lst )
            self.mobjsTOmove = list[self.FiboDot]()
        else:
            self.moveRoot(rootParrentIndex)
            self.add(pointer)

    def animateRoot(self, root: list[FiboDot], startIndex: int, removedDotCenter: Point3D): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        def aux (root: list, rootIndex: int, lastDotDestination: Dot):
            if rootIndex == len(root):
                return
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.FiboDot): #will be fixed by new vgroup
                return 
            currentDot.dot.target = Dot(point=currentDot.dot.get_center(), radius=currentDot.dot.radius, color=currentDot.dot.color)
            currentDot.dot.target.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.dot.radius*2).set_y(lastDotDestination.get_y())
            self.mobjsTOmove.append(currentDot)
            #if isinstance(currentDot.target, self.FiboDot):
            self.animateChildren(currentDot, currentDot.dot.target)
            
            aux(root, rootIndex+1, currentDot.dot.target)
            return

        startDot = Dot(removedDotCenter)
        if startIndex != 0:
            startDot = root[startIndex-1].dot

        aux(root, startIndex, startDot)
        return

    def moveRoot(self, rootIndexOfNewParrent: int):
        if rootIndexOfNewParrent == 0:
            rootDot = self.root[rootIndexOfNewParrent]
            self.moveChildren(rootDot)

        def aux (root: list[self.FiboDot], rootIndex: int, lastDotDestination: Dot):
            if rootIndex == len(root):
                return []
            
            currentDot = root[rootIndex]
            currentDot.dot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.dot.radius*2).set_y(lastDotDestination.get_y())

            self.moveChildren(currentDot)
            
            aux(root, rootIndex+1, currentDot.dot)

        (aux(self.root, 1, self.root[0].dot))
        return

    def animateChildren(self, parrentMojb: FiboDot, parrentTarget: FiboDot): #TODO need to be made into a transform method where it can collect all animation and then move.
        if len(parrentMojb.children)==0:
            return
        #listOfTargets = list()
        for n in parrentMojb.children:
            n.dot.target = Dot(point=n.dot.get_center(), radius=n.dot.radius, color=n.dot.color).set_y(parrentTarget.get_y()-1.5).align_to(parrentTarget, RIGHT)
            #listOfTargets.append(n)
            self.mobjsTOmove.append(n)
        self.space_list_dots_targets_by_tree_width(parrentMojb.children)
        #parrentMojb.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentTarget.get_y()-1.5).align_to(parrentTarget, RIGHT)
        #self.mobjsTOmove.append(parrentMojb.children)
        for n in range(len(parrentMojb.children)):
            self.animateChildren(parrentMojb.children[n], parrentMojb.children[n].dot.target)
        return
        
    def moveChildren(self, parrentMojb: FiboDot):
        if len(parrentMojb.children)==0:
            return
        #Fix
        #self.add(parrentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
        for n in parrentMojb.children:
            self.moveChildren(n)

    def delete(self, deleteDotID: int, isAnimation: bool):
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.getRootKeyIndex(self.root, deleteDotID)

        self.root.remove(deleteDot)
    
        childrenArrows = []
        if len(deleteDot.children)>0:
            deleteDot.children.reverse() #TODO should it be reversed? now that it isnt a Vgroup
            for n in deleteDot.children:
                childrenArrows.append(n.arrow)
                n.parrentKey = None
                self.root.add(n)

        if isAnimation:
            self.animateRoot(self.root, index, deleteDot.dot.get_center())
            self.play(AnimationGroup(*[MoveToTarget(n.dot) for n in self.mobjsTOmove], lag_ratio=0), AnimationGroup(*[FadeOut(n) for n in childrenArrows]), FadeOut(deleteDot.dot))#, FadeOut(deleteDot.numberLabel))
            self.mobjsTOmove = list[self.FiboDot]()
            self.adjust_camera(isAnimation)
        else:
            #self.remove(deleteDot.text)
            self.remove(deleteDot)
            self.moveRoot(index-1)
            for n in childrenArrows:
                self.remove(n)

    def moveToRoot(self, movingDotID: int, isAnimation: bool):
        movingDot = self.nodeDic.get(movingDotID)
        parrentDot = self.nodeDic.get(movingDot.parrentKey)

        movingDot.parrentKey = None
        parrentDot.children.remove(movingDot)
        self.root.add(movingDot)

        if isAnimation:
            self.animateRoot(self.root, len(self.root)-1)
            self.play(AnimationGroup(*[MoveToTarget(n.dot) for n in self.mobjsTOmove], lag_ratio=0), FadeOut(movingDot.arrow))
            self.mobjsTOmove = list[self.FiboDot]()
        else:
            self.moveRoot(self, len(self.root)-1)
            self.remove(movingDot.arrow)

    def setMin(self, min_id):
        min_node_index = self.getRootKeyIndex(self.root, min_id)
        if not isinstance(min_node_index, int):
            return
        minFiboNode = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.dot.fade_to(BLUE, 1)

        self.min_node = minFiboNode
        minFiboNode.dot.fade_to(RED, 100)

    def adjust_camera_after_consolidate(self):
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]

        if isinstance(mostLeftNode, self.FiboDot) and isinstance(mostRightNode, self.FiboDot):
            rightPoint = mostRightNode.dot.get_right()
            leftPoint = mostLeftNode.dot.get_left()

            self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2
            currentWidthOfHeap = rightPoint[0]-leftPoint[0]
            newWidth = self.width
            while newWidth < currentWidthOfHeap:
                newWidth = newWidth * 2
            
            if newWidth == self.width:
                self.multp = 0
            else: 
                self.multp = newWidth / self.width

            newCenter: Point3D = (((rightPoint[0]+leftPoint[0])/2), (self.multp * 2)*-1, (rightPoint[2]+leftPoint[2])/2)

            self.play(self.camera.frame.animate.move_to(newCenter).set(width=newWidth))

