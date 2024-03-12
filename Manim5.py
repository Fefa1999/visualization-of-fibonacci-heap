from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing import TypedDict

#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        self.min_node = None
        self.root = VGroup()
        self.dotsTOmove = list()
        self.nodeDic = dict()
        self.defaultAddPoint = [0,3, 0]
        self.height = 7.993754879000781                                                                                                                                                                                              
        self.width = 14.222222222222221
        self.multp = 0
        super().__init__(*args, **kwargs)

    #New dot class. A manim dot with children.
    class newDot(Dot):
        def __init__(self, id: int, *args, **kwargs):
            self.id = id
            super().__init__(*args, **kwargs)
            self.children = VGroup()
            self.widthOfChildren = int()
            self.parrentKey = int()
            self.arrow = Line()
            self.text = Text("")

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

    def get_root_key_index(self, root: VGroup, key: int):
        for n in range(len(root)):
            a = root[n]
            if isinstance(a, self.newDot):
                if a.id == key:
                    return n
        return

    #Creates a dot with a location, and return it withour adding it to scene.
    def createDot(self, point: Point3D, number: int, id: int):
        blue_dot = self.newDot(id, point, radius=0.2, color=BLUE)
        dot_label = Text(str(number), font_size=18 - (number/100)).move_to(blue_dot.get_center()).set_z_index(1) #TODO what is this number/100 
        dot_label.add_updater(
            lambda mobject: mobject.next_to(blue_dot, 0)
        )
        blue_dot.text = dot_label
        blue_dot.widthOfChildren = blue_dot.radius*2
        return blue_dot

    #Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
    def insertDot(self, number: int, fadeIn: bool, id: int):
        dot = self.createDot(self.defaultAddPoint, number, id)
        self.nodeDic[id] = dot

        self.root.add(dot)   #Gets inserted into root vgroup... should it be here?
        if fadeIn:
            self.play(FadeIn(dot, dot.text))
        else:
            self.add(dot, dot.text)

        self.moveToRootSpot(fadeIn)
        self.adjust_camera(fadeIn)
        return dot

    def moveToRootSpot(self, fadeIn: bool):
        rootlength = len(self.root)
        addedDot = self.root[rootlength-1]
        if rootlength == 1:
            if fadeIn:
                self.play(addedDot.animate.move_to([0, 2, 0]))
            else:
                addedDot.move_to([0, 2, 0])
        
        mostRightDot = self.root[rootlength-2]
        if isinstance(addedDot, self.newDot) and isinstance(mostRightDot, self.newDot):
            if fadeIn:
                self.play(addedDot.animate.next_to(mostRightDot, buff=2*mostRightDot.radius))
            else:
                addedDot.next_to(mostRightDot, buff=2*mostRightDot.radius)             

    # def adjust_camera(self, isAnimation):
    #     mostLeftNode = self.get_left_most_dot(self.root)
    #     mostRightNode = self.root[len(self.root)-1]

    #     if isinstance(mostLeftNode, self.newDot) and isinstance(mostRightNode, self.newDot):
    #         rightPoint = mostRightNode.get_right()
    #         leftPoint = mostLeftNode.get_left()

    #         newWidth = rightPoint[0]-leftPoint[0]
    #         self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2

    #         boarderRight = self.camera.frame.get_right()[0]
    #         boarderLeft = self.camera.frame.get_left()[0]
    #         #if not isinstance(boarderLeft, float) or not isinstance(boarderRight, float):
    #         #    return
            

    #         if newWidth+4 > (self.camera.frame_width) or boarderLeft > (leftPoint[0]+2) or boarderRight < (rightPoint[0]+2): # +4 is secureing padding
    #             self.multp = (self.camera.frame_width * 2) / self.width
    #             newCenter = (((rightPoint[0]+leftPoint[0])/2), (self.multp * 2)*-1, (rightPoint[2]+leftPoint[2])/2)
    #             if isAnimation:
    #                 self.play(self.camera.frame.animate.set(width=self.camera.frame_width * 2).move_to(newCenter))
    #             else: 
    #                 self.camera.frame.set(width=self.camera.frame_width * 2).move_to(newCenter)
                
    #             self.camera.frame.move_to(newCenter) #TODO make anmation also
    
    def get_left_most_dot(self, group: VGroup):
        if len(group) == 0:
            return
        
        def aux(a:  self.newDot):
            if len(a.children) > 0:
                return aux(a.children.submobjects[len(a.children)-1])
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

    def createChild(self, parrentKey: int, childKey: int, isAnimation: bool):
        rootParrentIndex = self.get_root_key_index(self.root, parrentKey)
        if not isinstance(rootParrentIndex, int):
            return
        parrentMojb = self.root[rootParrentIndex]

        rootChildIndex = self.get_root_key_index(self.root, childKey)
        if not isinstance(rootChildIndex, int):
            return
        childMojb = self.root[rootChildIndex]

        if isinstance(childMojb, self.newDot):
            childMojb.parrentKey = parrentKey

        if isinstance(parrentMojb, self.newDot):
            parrentMojb.children.add(childMojb)

            #creating arrow
            pointer = Line(childMojb,parrentMojb)
            pointer.add_updater(
                lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parrentMojb.get_bottom()) #TODO add custome scaller for width
                )
            childMojb.arrow = pointer

            self.root.remove(childMojb)
            childWidth = int() 
            if len(parrentMojb.children) == 1:
                childWidth = 0
            else:
                childWidth = childMojb.widthOfChildren + parrentMojb.radius*2
            parrentMojb.widthOfChildren = parrentMojb.widthOfChildren + childWidth

            if isAnimation:
                index = min(rootParrentIndex,rootChildIndex)
                
                self.animateRoot(self.root, index, self.root[index].get_center())
                self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsTOmove], lag_ratio=0), FadeIn(pointer))
                self.dotsTOmove = list()
            else:
                self.moveRoot(rootParrentIndex)
                self.add(pointer)

    def animateRoot(self, root: VGroup, startIndex, removedDotCenter): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return 
            currentDot.target = self.newDot(id=currentDot.id, point=currentDot.get_center(), radius=currentDot.radius, color=currentDot.color)
            currentDot.target.widthOfChildren = currentDot.widthOfChildren
            currentDot.target.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())
            self.dotsTOmove.append(currentDot)
            if isinstance(currentDot.target, self.newDot):
                self.animateChildren(currentDot, currentDot.target)
            
            aux(root, rootIndex+1, currentDot.target)
            return
        
        startDot = self.newDot(0, removedDotCenter)
        if startIndex != 0: #VGroups first index of subobjects is at 1
            startDot = root[startIndex-1]

        aux(root, startIndex, startDot)
        return

    def moveRoot(self, rootIndexOfNewParrent: int):
        if rootIndexOfNewParrent == 0:
            rootDot = self.root[rootIndexOfNewParrent]
            self.moveChildren(rootDot)

        
        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return []
            
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return []
            currentDot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())

            self.moveChildren(currentDot)
            
            aux(root, rootIndex+1, currentDot)

        (aux(self.root, 1, self.root[0]))
        return

    def animateChildren(self, parrentMojb: newDot, parrentTarget: newDot): #need to be made into a transform method where it can collect all animation and then move.
        if len(parrentMojb.children)==0:
            return
        parrentMojb.children.target = VGroup()
        for n in parrentMojb.children.submobjects:
            n.target = self.newDot(id=n.id, point=n.get_center(), radius=n.radius, color=n.color)
            n.target.widthOfChildren = n.widthOfChildren
            parrentMojb.children.target.add(n.target)
        parrentMojb.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentTarget.get_y()-1).align_to(parrentTarget, RIGHT)
        self.dotsTOmove.append(parrentMojb.children)
        for n in range(len(parrentMojb.children)):
            self.animateChildren(parrentMojb.children[n], parrentMojb.children.target[n])
        return
        
    def moveChildren(self, parrentMojb: newDot):
        if len(parrentMojb.children)==0:
            return
        self.add(parrentMojb.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parrentMojb.get_y()-1).align_to(parrentMojb, RIGHT))
        for n in parrentMojb.children:
            self.moveChildren(n)

    def delete(self, deleteDotID: int, isAnimation: bool):
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.get_root_key_index(self.root, deleteDotID)

        self.root.remove(deleteDot)
    
        childrenArrows = []
        if len(deleteDot.children)>0:
            deleteDot.children.submobjects.reverse()
            for n in deleteDot.children.submobjects:
                childrenArrows.append(n.arrow)
                n.parrentKey = None
                self.root.add(n)

        if isAnimation:
            self.animateRoot(self.root, index, deleteDot.get_center())
            self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsTOmove], lag_ratio=0), AnimationGroup(*[FadeOut(n) for n in childrenArrows]), FadeOut(deleteDot.text), FadeOut(deleteDot))
            self.dotsTOmove = list()
            self.adjust_camera(isAnimation)
        else:
            self.remove(deleteDot.text)
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
            self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsTOmove], lag_ratio=0), FadeOut(movingDot.arrow))
            self.dotsTOmove = list()
        else:
            self.moveRoot(self, len(self.root)-1)
            self.remove(movingDot.arrow)

    def setMin(self, min_id):
        min_node_index = self.get_root_key_index(self.root, min_id)
        if not isinstance(min_node_index, int):
            return
        min_node = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.fade_to(BLUE, 1)

        self.min_node = min_node
        min_node.fade_to(RED, 100)

    def adjust_camera(self, isAnimation):
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]

        if isinstance(mostLeftNode, self.newDot) and isinstance(mostRightNode, self.newDot):
            rightPoint = mostRightNode.get_right()
            leftPoint = mostLeftNode.get_left()
            self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2
            currentWidthOfHeap = rightPoint[0]-leftPoint[0]
            newCenter = [((rightPoint[0]+leftPoint[0])/2), (self.multp * 2)*-1, (rightPoint[2]+leftPoint[2])/2]
            if currentWidthOfHeap+2.4 > (self.camera.frame_width):
                self.zoom_out(isAnimation, newCenter)      
            elif currentWidthOfHeap < self.camera.frame_width - self.width:
                self.zoom_in(isAnimation, newCenter, currentWidthOfHeap)
            else:
                if(isAnimation):
                    self.play(self.camera.frame.animate.move_to(newCenter))
                else:
                    self.camera.frame.move_to(newCenter)

    def zoom_in(self, isAnimation, newCenter, currentWidthOfHeap):
        newWidth = self.width
        while newWidth < currentWidthOfHeap:
            newWidth = newWidth + self.width
        
        if newWidth == self.width:
            self.multp = 0
        else: 
            self.multp = newWidth / self.width

        newCenter[1] = (self.multp * 2)*-1
        if isAnimation:
            self.play(self.camera.frame.animate.move_to(newCenter).set(width=newWidth))
        else:
            self.camera.frame.move_to(newCenter).set(width=newWidth)

    def zoom_out(self, isAnimation, newCenter):
        self.multp = self.multp+1
        if isAnimation:
            self.play(self.camera.frame.animate.set(width=self.camera.frame_width + self.width).move_to(newCenter))
        else: 
            self.camera.frame.set(width=self.camera.frame_width + self.width).move_to(newCenter)