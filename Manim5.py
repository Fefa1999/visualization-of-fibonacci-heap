from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing import Self
from typing import TypedDict

#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER
#HOW DOES MANIM HANDLE REMOVED OBJECTS? ARE THEY DELTED?

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        self.min_node: self.FiboDot = None
        self.root = list[self.FiboDot]()
        self.mobjsTOmove = list[self.FiboDot]()
        self.storedAnimations = list[Animation]()
        self.nodeDic = dict[int, self.FiboDot]()
        self.sceneUpToDate = True
        self.showLabels = True
        self.defaultAddPoint = [0.0, 3.0, 0.0]
        self.height = 7.993754879000781                                                                                                                                                                                              
        self.width = 14.222222222222221
        self.multp = 0
        super().__init__(*args, **kwargs)
    
    def construct(self):
        #self.adjust_camera(True)
        self.wait(5)
        self.clear()
        #dot_label = Text(str("THANKS FOR WATCHING"), font_size=25).move_to(self.camera.frame.get_center())
        #self.play(FadeIn(dot_label))

    #New dot class. A manim dot with children.
    class FiboDot:
        dot: Dot
        id: int
        parentKey: int
        children: list[Self]
        widthOfChildren: int
        dot: Dot
        arrow: Line = None
        numberLabel: Text
        #target: Point3D #Not used ATM
        def __init__(self, idKey: int):
            self.id = idKey
            self.parentKey = None
            self.children = list[Self]()
            #self.widthOfChildren = int()
            #self.arrow = Line()
            #self.numberLabel = Text("")
    

    def space_list_dots_by_tree_width(self, lst: list[FiboDot], isToTarget: bool, direction: Vector3 = LEFT, **kwargs):
        if isToTarget:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren), **kwargs)
        else:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.next_to(m1.dot, direction, (m1.widthOfChildren), **kwargs)
        return lst

    def get_root_key_index(self, root: list, key: int):
        for n in range(len(root)):
            a = root[n]
            if a.id == key:
                return n
        return -1

    #Creates a FiboDot with a dot at "location", and numberLabel showing numberl, and return it without adding it to scene.
    def create_dot(self, point: Point3D, number: int, id: int):
        fiboDot = self.FiboDot(id)
        fiboDot.dot = Dot(point, radius=0.2, color=BLUE)
        fiboDot.numberLabel = Text(str(number), font_size=18).move_to(fiboDot.dot.get_center()).set_z_index(1) #Why is set_z_index soooo slow? #And Stroke width???
        fiboDot.widthOfChildren = fiboDot.dot.radius*2
        return fiboDot

    #Inserts the dot onto the scene and adds it to a vgroup (Root), then calls for a repositioning of the nodes.
    def insert_dot(self, number: int, isAnimation: bool, id: int):
        self.prepareSceneForAnimations(isAnimation)

        fiboDot = self.create_dot(self.defaultAddPoint, number, id)
        self.nodeDic[id] = fiboDot
        self.root.append(fiboDot)

        if isAnimation:
            if self.showLabels:
                self.play(FadeIn(fiboDot.dot, fiboDot.numberLabel))
            else:
                self.play(FadeIn(fiboDot.dot))
        else:
            if self.showLabels:
                self.add(fiboDot.dot, fiboDot.numberLabel)
            else:
                self.add(fiboDot.dot)

        if len(self.root) == 1:
            if isAnimation:
                self.play(fiboDot.dot.animate.move_to([0.0, 2.0, 0.0]), fiboDot.numberLabel.animate.move_to([0.0, 2.0, 0.0]))
                return
            else:
                fiboDot.dot.move_to([0.0, 2.0, 0.0])
                fiboDot.numberLabel.move_to([0.0, 2.0, 0.0])
                return

        if isAnimation:
            self.animate_root((len(self.root)-1))
        else:
            self.sceneUpToDate = False

    def adjust_camera(self, isAnimation): #Fix should have soooo many lookups.
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]

        rightPoint = mostRightNode.dot.get_right()
        leftPoint = mostLeftNode.dot.get_left()

        newWidth = rightPoint[0]-leftPoint[0]
        self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2
        self.defaultAddPoint[1] = rightPoint[1]+1.0

        boarderRight = self.camera.frame.get_right()[0]
        boarderLeft = self.camera.frame.get_left()[0]

        newCenter = (((rightPoint[0]+leftPoint[0])/2), ((rightPoint[1]+leftPoint[1])/2), ((rightPoint[2]+leftPoint[2])/2))
        #Only zoomes out
        if newWidth+2 > (self.camera.frame_width) or boarderLeft > (leftPoint[0]+1) or boarderRight < (rightPoint[0]+1): # +2 is secureing padding
            if isAnimation:
                self.play(self.camera.frame.animate.set(width=self.camera.frame_width * 1.3).move_to(newCenter))
            else: 
                self.camera.frame.set(width=self.camera.frame_width * 1.3).move_to(newCenter)
        elif (self.camera.frame.get_width()/5)<abs(newCenter[0]-self.camera.frame.get_center()[0]) or (self.camera.frame.get_height()/5)<abs(newCenter[1]-self.camera.frame.get_center()[1]):
            if isAnimation:
                self.play(self.camera.frame.animate.set(width=self.camera.frame_width * 1.3).move_to(newCenter))
            else: 
                self.camera.frame.set(width=self.camera.frame_width * 1.3).move_to(newCenter)

        
    def get_left_most_dot(self, group: list[FiboDot]):
        if len(group) == 0:
            return #TODO should it return something to tell it failed??
        
        def aux(a: self.FiboDot):
            if len(a.children) > 0:
                return aux(a.children[len(a.children)-1])
            else:
                return a
        
        return aux(group[0])

      
    def create_child(self, parentKey: int, childKey: int, isAnimation: bool, showExplanatoryText: bool = False):
        self.prepareSceneForAnimations(isAnimation)

        #Finding parent and child
        rootParrentIndex = self.get_root_key_index(self.root, parentKey)
        if rootParrentIndex<0:
            return  #TODO should it return something to tell it failed??
        parentMobj = self.root[rootParrentIndex]
        rootChildIndex = self.get_root_key_index(self.root, childKey)
        if rootChildIndex<0:
            return  #TODO should it return something to tell it failed??
        childMojb = self.root[rootChildIndex]
        childMojb.parentKey = parentKey
        
        #Adding child to parent and removing from root
        parentMobj.children.append(childMojb)
        self.root.remove(childMojb)

        #creating arrow
        pointer = Line(childMojb.dot,parentMobj.dot).set_z_index(-1)
        childMojb.arrow = pointer

        #Calculation new widths.
        self.update_widthOfChildren(parentMobj, childMojb, isAddingNode=True)

        if showExplanatoryText and isAnimation:
           text = "Compare " + str(parentMobj.id) + " < " + str(childMojb.id) + " and move " + str(childMojb.id) + " as a child of " + str(parentMobj.id)
           textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
           explanatoryText = Text(str(text), font_size=18).move_to(textPlacement)
           self.play(FadeIn(explanatoryText))
        
        if isAnimation:
            self.storedAnimations.append(FadeIn(pointer))
            firstIndexOfChange = min(rootParrentIndex,rootChildIndex)
            self.animate_root(firstIndexOfChange)
        else:
            self.add(pointer)
            self.sceneUpToDate = False
            
        if showExplanatoryText and isAnimation:
            self.play(FadeOut(explanatoryText))

    def update_widthOfChildren(self, parent: FiboDot, child: FiboDot, isAddingNode: bool):
        if isAddingNode:
            gainedWidth = int() 
            if len(parent.children) == 1:
                gainedWidth = 0
            else:
                gainedWidth = child.widthOfChildren + parent.dot.radius*2
            parent.widthOfChildren = parent.widthOfChildren + gainedWidth
        else:
            #If we remove a child in the middle of a tree, the tree should "move together" and become more narrow
            Temp_node = parent
            while isinstance(Temp_node, self.FiboDot):
                Temp_node.widthOfChildren = Temp_node.widthOfChildren - child.widthOfChildren
                Temp_node = self.nodeDic.get(Temp_node.parentKey)   
            
    def animate_root(self, startIndex: int): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        self.prepareSceneForAnimations(True)

        if startIndex >= len(self.root): #this can happen if the last insered dot in root is removed
            self.executeStoredAnimations()
            self.remove_label_check()
            self.adjust_camera(True)
            return

        def aux (rootIndex: int, lastDotDestination: Point3D):
            if rootIndex == len(self.root):
                return
            currentDot = self.root[rootIndex]
            if not isinstance(currentDot, self.FiboDot): #TODO why is this still needed?
                return 
            currentDot.dot.target = Dot(point=currentDot.dot.get_center(), radius=currentDot.dot.radius, color=currentDot.dot.color)
            currentDot.dot.target.set_x(lastDotDestination[0]+currentDot.widthOfChildren+currentDot.dot.radius*2).set_y(lastDotDestination[1])
            self.mobjsTOmove.append(currentDot)
            self.create_children_animations(currentDot, currentDot.dot.target)
            
            aux(rootIndex+1, currentDot.dot.target.get_center())
            return

        rootNodeAtIndex = self.root[startIndex]
        leftRootDotLocation: Point3D
        if startIndex == 0: 
            self.create_children_animations(rootNodeAtIndex, rootNodeAtIndex.dot)
            rootNodeAtIndex.dot.target = Dot(point=rootNodeAtIndex.dot.get_center(), radius=rootNodeAtIndex.dot.radius, color=rootNodeAtIndex.dot.color)
            self.mobjsTOmove.append(rootNodeAtIndex)
            leftRootDotLocation = rootNodeAtIndex.dot.get_center()
            startIndex += 1
        else: 
            leftRootDotLocation = self.root[startIndex-1].dot.get_center()

        aux(startIndex, leftRootDotLocation)

        self.buildAnimation()
        self.executeStoredAnimations()
        self.remove_label_check()
        self.adjust_camera(True)
        return

    def create_children_animations(self, parentMojb: FiboDot, parentTarget: Dot):
        if len(parentMojb.children)==0:
            return

        #First child which the other children should be alinged left of
        baseChild = parentMojb.children[0]
        baseChild.dot.target = Dot(point=baseChild.dot.get_center(), radius=baseChild.dot.radius, color=baseChild.dot.color).set_y(parentTarget.get_y()-1.5).align_to(parentTarget, RIGHT)
        self.mobjsTOmove.append(baseChild)

        for i in range(len(parentMojb.children)-1):
            child =  parentMojb.children[i+1]
            child.dot.target = Dot(point=child.dot.get_center(), radius=child.dot.radius, color=child.dot.color)
            self.mobjsTOmove.append(child)
        
        #Arrange based on first child.
        self.space_list_dots_by_tree_width(parentMojb.children, True)

        for n in range(len(parentMojb.children)):
            self.create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target)
        return
    
    def build_scene(self, startIndex: int):
        if startIndex == 0:
            rootDot = self.root[startIndex]
            self.move_children(rootDot)
            startIndex += 1

        def aux (root: list[self.FiboDot], rootIndex: int, lastDotDestination: Dot):
            if rootIndex == len(root):
                return []
            
            currentDot = root[rootIndex]
            currentDot.dot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.dot.radius*2).set_y(lastDotDestination.get_y())
            
            if self.showLabels:
                currentDot.numberLabel.move_to(currentDot.dot.get_center())

            self.move_children(currentDot)
            
            aux(root, rootIndex+1, currentDot.dot)

        aux(self.root, startIndex, self.root[startIndex-1].dot)
        self.remove_label_check()
        self.adjust_camera(False)
        return
        
    def move_children(self, parentMojb: FiboDot):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        parentMojb.children[0].dot.set_y(parentMojb.dot.get_y()-1).align_to(parentMojb.dot, RIGHT)
        
        #Arrange rest based on first
        self.space_list_dots_by_tree_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)
            self.move_children(n)

    def delete(self, deleteDotID: int, isAnimation: bool):
        self.prepareSceneForAnimations(isAnimation)
        
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.get_root_key_index(self.root, deleteDotID)

        self.root.remove(deleteDot)
    
        childrenArrows = []
        if (len(deleteDot.children)>0):
            deleteDot.children.reverse()
            for n in deleteDot.children:
                childrenArrows.append(n.arrow)
                n.arrow = None
                n.parentKey = None
                self.root.append(n)

        self.nodeDic.pop(deleteDot.id)  #No test if it works
        if isAnimation:
            for n in childrenArrows:
                self.storedAnimations.append(FadeOut(n))
            self.storedAnimations.append(FadeOut(deleteDot.dot))
            if self.showLabels:
                self.storedAnimations.append(FadeOut(deleteDot.numberLabel))
            self.animate_root(index)
        else:
            if self.showLabels:
                self.remove(deleteDot.numberLabel)
            self.remove(deleteDot.dot)
            for n in childrenArrows:
                self.remove(n)
            self.sceneUpToDate = False
        

    def set_min(self, min_id):
        min_node_index = self.get_root_key_index(self.root, min_id)
        if not isinstance(min_node_index, int):
            return
        minFiboNode = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.dot.color = BLUE

        self.min_node = minFiboNode
        minFiboNode.dot.color = RED

    def buildAnimation(self):
        listOfAnimations = list[Animation]()
        for n in self.mobjsTOmove:
            listOfAnimations.append(MoveToTarget(n.dot))
            if self.showLabels:
                listOfAnimations.append(n.numberLabel.animate.move_to(n.dot.target.get_center()))
            if not (n.arrow is None):
                listOfAnimations.append(n.arrow.animate.put_start_and_end_on(n.dot.target.get_top(), self.nodeDic[n.parentKey].dot.target.get_bottom()))
            n.target = None
        self.mobjsTOmove = list[self.FiboDot]()
        self.storedAnimations.extend(listOfAnimations)
        return 

    def executeStoredAnimations(self):
        self.play(*self.storedAnimations)
        self.storedAnimations = list[Animation]()
        return

    def adjust_camera_after_consolidate(self, isAnimation: bool): #TODO THIS IS NEVER USED. should have soooo many lookups.
        self.prepareSceneForAnimations(isAnimation)
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]

        if isinstance(mostLeftNode, self.FiboDot) and isinstance(mostRightNode, self.FiboDot):
            rightPoint = mostRightNode.dot.get_right()
            leftPoint = mostLeftNode.dot.get_left()
            self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2
            self.defaultAddPoint[1] = rightPoint[1]+1.0
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
        self.prepareSceneForAnimations(isAnimation)
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
        self.prepareSceneForAnimations(isAnimation)
        self.multp = self.multp+1
        if isAnimation:
            self.play(self.camera.frame.animate.set(width=self.camera.frame_width + self.width).move_to(newCenter))
        else: 
            self.camera.frame.set(width=self.camera.frame_width + self.width).move_to(newCenter)

    def change_key(self, nodeId, newValue: int, isAnimation: bool, showExplanatoryText: bool=False):
        self.prepareSceneForAnimations(isAnimation)

        node = self.nodeDic[nodeId]
        new_text = Text(str(newValue), font_size=18 - (newValue/100)).move_to(node.dot.get_center()).set_z_index(1) #TODO why not just change the text???
        if showExplanatoryText:
            text = "Decrease key of node " + str(node.id) + " to " + str(newValue)
            self.write_explanatory_text_to_video(text)
        if isAnimation:
            if self.showLabels:
                self.play(FadeOut(node.numberLabel), FadeIn(new_text))
            #self.play(Transform(node.numberLabel, new_text)) #more expensive? and leaves the other the screen
            node.numberLabel = new_text
        else:
            node.numberLabel.become(new_text)

    def cut(self, node_to_cut_ID: int, isAnimation: bool, unMark, showExplanatoryText: bool=False):
        self.prepareSceneForAnimations(isAnimation)
        node_to_cut = self.nodeDic[node_to_cut_ID]
        if showExplanatoryText:
            text = "Cut " + node_to_cut.numberLabel.text + " from parent and move it to the root list"
            self.write_explanatory_text_to_video(text)

        parent_node = self.nodeDic[node_to_cut.parentKey]
        arrowToBeRemoved = node_to_cut.arrow
        node_to_cut.arrow = None
        node_to_cut.parentKey = None
        parent_node.children.remove(node_to_cut)
        self.root.append(node_to_cut)
        
        self.update_widthOfChildren(parent_node, node_to_cut, isAddingNode=False)

        firstIndexOfChange = self.get_root_key_index(self.root, parent_node.id) #TODO Doesnt work if parent not in root.
        print(firstIndexOfChange)
        if isAnimation:
            self.storedAnimations.append(FadeOut(arrowToBeRemoved))
            self.animate_root(firstIndexOfChange)
        else:
            self.remove(arrowToBeRemoved)
            self.sceneUpToDate = False

        if unMark and showExplanatoryText:
            text = "If " + node_to_cut.numberLabel.text + " is marked, unmark it again"
            self.write_explanatory_text_to_video(text)
            if isAnimation:
                self.play(node_to_cut.dot.animate.set_color(BLUE))
            else:
                node_to_cut.dot.color = BLUE
        
    def cascading_cut(self, decreased_node_parent_id, isAnimation, showExplanatoryText):
        self.prepareSceneForAnimations(isAnimation)
        node = self.nodeDic[decreased_node_parent_id]
        if showExplanatoryText:
            self.write_explanatory_text_to_video("If parent is unmarked, mark it")
        if isAnimation:
            self.play(node.dot.animate.set_color(ORANGE))
        else:
            node.dot.color = ORANGE
    
    def write_explanatory_text_to_video(self, text):
        textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
        explanatoryText = Text(str(text), font_size=30).move_to(textPlacement)
        self.play(FadeIn(explanatoryText))
        self.play(FadeOut(explanatoryText))

    def remove_label_check(self): #low quality: 35 dots - medium: ??- High: 65 dots - Production: 97 - 4k: 110 
        qualityNumber = 200
        numberOfDots = len(self.nodeDic.values())
        if numberOfDots >= qualityNumber and self.showLabels:
            self.showLabels = False
            self.remove_labels()
        elif (numberOfDots < qualityNumber) and not self.showLabels:
            self.showLabels = True
            self.add_labels()
        
    def add_labels(self):
        for _, n in self.nodeDic.items():
            self.add(n.numberLabel.move_to(n.dot.get_center()))
        return

    def remove_labels(self):
        for _, n in self.nodeDic.items():
            self.remove(n.numberLabel)
        return
        
    def prepareSceneForAnimations(self, isAnimation: bool):
        if not isAnimation or self.sceneUpToDate:
            return
        self.build_scene(0)
        self.sceneUpToDate = True