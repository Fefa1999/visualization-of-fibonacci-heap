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
        self.dotsToMove = list()
        self.nodeDic = dict()
        self.defaultAddPoint = [0,3, 0]
        self.height = 7.993754879000781                                                                                                                                                                                              
        self.width = 14.222222222222221
        self.multp = 0
        super().__init__(*args, **kwargs)
    
    def construct(self):
        self.adjust_camera(True)
        self.wait(5)
        self.clear()
        dot_label = Text(str("THANKS FOR WATCHING"), font_size=25).move_to(self.camera.frame.get_center())
        self.play(FadeIn(dot_label))

    #New dot class. A manim dot with children.
    class newDot(Dot):
        def __init__(self, id: int, *args, **kwargs):
            self.id = id
            super().__init__(*args, **kwargs)
            self.children = VGroup()
            self.widthOfChildren = int()
            self.parentKey = None
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
    def create_dot(self, point: Point3D, number: int, id: int):
        blue_dot = self.newDot(id, point, radius=0.2, color=BLUE)
        dot_label = Text(str(number), font_size=18 - (number/100)).move_to(blue_dot.get_center()).set_z_index(1) #TODO what is this number/100 
        dot_label.add_updater(
            lambda mobject: mobject.next_to(blue_dot, 0)
        )
        blue_dot.text = dot_label
        blue_dot.widthOfChildren = blue_dot.radius*2
        return blue_dot

    #Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
    def insert_dot(self, number: int, fadeIn: bool, id: int):
        dot = self.create_dot(self.defaultAddPoint, number, id)
        self.nodeDic[id] = dot

        self.root.add(dot)   #Gets inserted into root vgroup... should it be here?
        if fadeIn:
            self.play(FadeIn(dot, dot.text))
        else:
            self.add(dot, dot.text)

        self.move_to_rootSpot(fadeIn)
        self.adjust_camera(fadeIn)
        return dot

    def move_to_rootSpot(self, fadeIn: bool):
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

    def create_child(self, parentKey: int, childKey: int, isAnimation: bool, showExplanatoryText: bool):
        rootParentIndex = self.get_root_key_index(self.root, parentKey)
        if not isinstance(rootParentIndex, int):
            return
        parentMobj = self.root[rootParentIndex]
        rootChildIndex = self.get_root_key_index(self.root, childKey)
        if not isinstance(rootChildIndex, int):
            return
        childMojb = self.root[rootChildIndex]
        if showExplanatoryText:
            text = "Compare " + str(parentMobj.id) + " < " + str(childMojb.id) + " and move " + str(childMojb.id) + " as a child of " + str(parentMobj.id)
            textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
            explanatoryText = Text(str(text), font_size=18).move_to(textPlacement)
            self.play(FadeIn(explanatoryText))
        if isinstance(childMojb, self.newDot):
            childMojb.parentKey = parentKey

        if isinstance(parentMobj, self.newDot):
            parentMobj.children.add(childMojb)

            #creating arrow
            pointer = Line(childMojb,parentMobj)
            pointer.add_updater(
                lambda mob: mob.put_start_and_end_on(childMojb.get_top(), parentMobj.get_bottom()) #TODO add custome scaller for width
                )
            childMojb.arrow = pointer

            self.root.remove(childMojb)
            self.update_child_width(parentMobj, childMojb, True)

            if isAnimation:
                index = min(rootParentIndex,rootChildIndex)
                self.animate_root(self.root, index, self.root[index].get_center())
                self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsToMove], lag_ratio=0), FadeIn(pointer))
                self.dotsToMove = list()
            else:
                self.move_root(rootParentIndex)
                self.add(pointer)
            if showExplanatoryText:
                self.play(FadeOut(explanatoryText))
        self.adjust_camera(isAnimation)
                
    def update_child_width(self, parent, child, plus):
        childWidth = int() 
        if plus:
            if len(parent.children) == 1:
                childWidth = 0
            else:
                childWidth = child.widthOfChildren + parent.radius*2
            parent.widthOfChildren = parent.widthOfChildren + childWidth
        else:
            #If we remove a child in the middle of a tree, the tree should "move together" and become more narrow
            Temp_node = parent
            while True:
                Temp_node.widthOfChildren = Temp_node.widthOfChildren - child.widthOfChildren
                if Temp_node.parentKey is None:
                    break
                Temp_node = self.nodeDic.get(Temp_node.parentKey)
            self.move_children(Temp_node)
            self.animate_root(self.root, self.get_root_key_index(self.root, Temp_node.id), Temp_node.get_center())
            self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsToMove], lag_ratio=0))
            self.dotsToMove = list()

    def animate_root(self, root: VGroup, startIndex, removedDotCenter): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return 
            currentDot.target = self.newDot(id=currentDot.id, point=currentDot.get_center(), radius=currentDot.radius, color=currentDot.color)
            currentDot.target.widthOfChildren = currentDot.widthOfChildren
            currentDot.target.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())
            self.dotsToMove.append(currentDot)
            if isinstance(currentDot.target, self.newDot):
                self.animate_children(currentDot, currentDot.target)
            
            aux(root, rootIndex+1, currentDot.target)
            return
        
        startDot = self.newDot(0, removedDotCenter)
        if startIndex != 0: #VGroups first index of subobjects is at 1
            startDot = root[startIndex-1]

        aux(root, startIndex, startDot)
        return

    def move_root(self, rootIndexOfNewParent: int):
        if rootIndexOfNewParent == 0:
            rootDot = self.root[rootIndexOfNewParent]
            self.move_children(rootDot)

        def aux (root: VGroup, rootIndex: int, lastDotDestination: self.newDot):
            if rootIndex == len(root):
                return []
            
            currentDot = root[rootIndex]
            if not isinstance(currentDot, self.newDot): #will be fixed by new vgroup
                return []
            currentDot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.radius*2).set_y(lastDotDestination.get_y())

            self.move_children(currentDot)
            
            aux(root, rootIndex+1, currentDot)

        (aux(self.root, 1, self.root[0]))
        return

    def animate_children(self, parentMobj: newDot, parentTarget: newDot): #need to be made into a transform method where it can collect all animation and then move.
        if len(parentMobj.children)==0:
            return
        parentMobj.children.target = VGroup()
        for n in parentMobj.children.submobjects:
            n.target = self.newDot(id=n.id, point=n.get_center(), radius=n.radius, color=n.color)
            n.target.widthOfChildren = n.widthOfChildren
            parentMobj.children.target.add(n.target)
        parentMobj.children.target.arrange_where_buffer_is_subtree_width(center= False).set_y(parentTarget.get_y()-1).align_to(parentTarget, RIGHT)
        self.dotsToMove.append(parentMobj.children)
        for n in range(len(parentMobj.children)):
            self.animate_children(parentMobj.children[n], parentMobj.children.target[n])

        
    def move_children(self, parentMobj: newDot):
        if len(parentMobj.children)==0:
            return
        self.add(parentMobj.children.arrange_where_buffer_is_subtree_width(center= False).set_y(parentMobj.get_y()-1).align_to(parentMobj, RIGHT))
        for n in parentMobj.children:
            self.move_children(n)

    def delete(self, deleteDotID: int, isAnimation: bool):
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.get_root_key_index(self.root, deleteDotID)

        self.root.remove(deleteDot)
    
        childrenArrows = []
        if len(deleteDot.children)>0:
            deleteDot.children.submobjects.reverse()
            for n in deleteDot.children.submobjects:
                childrenArrows.append(n.arrow)
                n.parentKey = None
                self.root.add(n)

        if isAnimation:
            self.animate_root(self.root, index, deleteDot.get_center())
            self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsToMove], lag_ratio=0), AnimationGroup(*[FadeOut(n) for n in childrenArrows]), FadeOut(deleteDot.text), FadeOut(deleteDot))
            self.dotsToMove = list()
            self.adjust_camera(isAnimation)
        else:
            self.remove(deleteDot.text)
            self.remove(deleteDot)
            self.move_root(index-1)
            for n in childrenArrows:
                self.remove(n)
        self.adjust_camera(isAnimation)

    def move_to_root(self, movingDotID: int, isAnimation: bool):
        movingDot = self.nodeDic.get(movingDotID)
        parentDot = self.nodeDic.get(movingDot.parentKey)
        movingDot.parentKey = None
        self.add(movingDot)
        parentDot.children.remove(movingDot)
        self.root.add(movingDot)
        index = self.get_root_key_index(self.root, movingDot.id)

        if isAnimation:
            self.animate_root(self.root, len(self.root)-1, movingDot.get_center())
            self.play(AnimationGroup(*[MoveToTarget(n) for n in self.dotsToMove], lag_ratio=0), FadeOut(movingDot.arrow))
            self.dotsToMove = list()
        else:
            self.move_root(index-1)
            self.remove(movingDot.arrow)
        self.adjust_camera(isAnimation)

    def set_min(self, min_id):
        min_node_index = self.get_root_key_index(self.root, min_id)
        if not isinstance(min_node_index, int):
            return
        min_node = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.color = BLUE

        self.min_node = min_node
        min_node.color = RED

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

    def change_key(self, nodeId, newValue, isAnimation, showExplanatoryText):
        node = self.nodeDic[nodeId]
        new_text = Text(str(newValue), font_size=18 - (newValue/100)).move_to(node.get_center()).set_z_index(1) 
        if showExplanatoryText:
            text = "Decrease key of node " + str(node.id) + " to " + str(newValue)
            self.write_explanatory_text_to_video(text)
        if isAnimation:
            self.play(Transform(node.text, new_text))
            node.text = new_text
        else:
            node.text.become(new_text)

    def cut(self, node_to_cut, isAnimation, unMark, showExplanatoryText):
        node = self.nodeDic[node_to_cut]
        if showExplanatoryText:
            text = "Cut " + node.text.text + " from parent and move it to the root list"
            self.write_explanatory_text_to_video(text)

        parent_node = self.nodeDic[node.parentKey]
        
        self.move_to_root(node_to_cut, isAnimation)
        self.update_child_width(parent_node, node, False)

        if unMark and showExplanatoryText:
            text = "If " + node.text.text + " is marked, unmark it again"
            self.write_explanatory_text_to_video(text)
        if isAnimation:
            self.play(node.animate.set_color(BLUE))
        else:
            node.color = BLUE
        
    def cascading_cut(self, decreased_node_parent_id, isAnimation, showExplanatoryText):
        node = self.nodeDic[decreased_node_parent_id]
        if showExplanatoryText:
            self.write_explanatory_text_to_video("If parent is unmarked, mark it")
        if isAnimation:
            self.play(node.animate.set_color(ORANGE))
        else:
            node.color = ORANGE
    
    def write_explanatory_text_to_video(self, text):
        textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
        explanatoryText = Text(str(text), font_size=30).move_to(textPlacement)
        self.play(FadeIn(explanatoryText))
        self.play(FadeOut(explanatoryText))