from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing_extensions import Self
from typing import TypedDict


#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER
#HOW DOES MANIM HANDLE REMOVED OBJECTS? ARE THEY DELTED?

class TreeLayout(Enum):
    RightAlligned = 1
    Balanced = 2
    H_V = 3

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        #For node tree
        self.min_node: self.FiboDot = None
        self.root = list[self.FiboDot]()
        self.nodeDic = dict[int, self.FiboDot]()

        #For Animations and Display
        self.rootSpot = [0.0, 2.0, 0.0]
        self.defaultAddPoint = [0.0, 3.0, 0.0]
        self.treeLayout = TreeLayout(1)
        self.sceneUpToDate = True
        self.showLabels = True
        self.mobjsTOmove = list[self.FiboDot]()
        self.storedAnimations = list[Animation]()
        
        #For Camera
        self.bottom_node = None
        self.height = 7.993754879000781                                                                                                                                                                                              
        self.width = 14.222222222222221
        self.multp = 0
        super().__init__(*args, **kwargs)
    
    def construct(self):
        self.clear()

    #New class. Contains an ID and a parrentKey for the fibonacci heap to indenfify and modify individual instanses. 
        #Contains a manim dot, line and text. All needed for manim to display a node.
        #Contains a list of children, width and heigth of them. For calculating mobjects target location.
    class FiboDot:
        id: int
        parentKey: int
        children: list[Self]
        widthOfChildren: int
        heigthOfChildren: int
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


    ################################################################
    ################### Fibonacci Heap Functions ###################
    #Creates a FiboDot with a dot at "location", and numberLabel showing numberl, and return it without adding it to scene.
    def create_dot(self, point: Point3D, number: int, id: int):
        fiboDot = self.FiboDot(id)
        fiboDot.dot = Dot(point, radius=0.2, color=BLUE)
        fiboDot.numberLabel = Text(str(number), font_size=18 - (number/100)).move_to(fiboDot.dot.get_center()).set_z_index(1)
        fiboDot.widthOfChildren = 0
        fiboDot.heigthOfChildren = 0
        return fiboDot

    #Inserts the dot onto the scene and adds it to a root list, then calls for a repositioning of the nodes.
    def insert_dot(self, number: int, isAnimation: bool, id: int):
        self.prepare(isAnimation)

        if isAnimation:
            fiboDot = self.create_dot(self.defaultAddPoint, number, id)
        else:
            fiboDot = self.create_dot(self.rootSpot, number, id)
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

        if len(self.root) == 1: #TODO this i propperly layout sensitive
            if isAnimation:
                self.play(fiboDot.dot.animate.move_to(self.rootSpot), fiboDot.numberLabel.animate.move_to(self.rootSpot))
                return
            else:
                fiboDot.dot.move_to(self.rootSpot)
                fiboDot.numberLabel.move_to(self.rootSpot)
                return

        if isAnimation:
            self.animateMovement((len(self.root)-1))
            self.adjust_camera(isAnimation)
        else:
            self.sceneUpToDate = False
        
        self.finish(isAnimation)

    def create_child(self, parentKey: int, childKey: int, isAnimation: bool, showExplanatoryText: bool = False):
        self.prepare(isAnimation)

        #Finding parent and child
        rootParrentIndex = self.get_root_index_from_key(self.root, parentKey)
        if rootParrentIndex<0:
            return  #TODO should it return something to tell it failed??
        parentMobj = self.root[rootParrentIndex]
        rootChildIndex = self.get_root_index_from_key(self.root, childKey)
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
        self.update_widthOfChildren(parentMobj, childMojb, isAddingNode=True) #TODO not layout sensitive

        if showExplanatoryText and isAnimation:
           text = "Compare " + str(parentMobj.id) + " < " + str(childMojb.id) + " and move " + str(childMojb.id) + " as a child of " + str(parentMobj.id)
           textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
           explanatoryText = Text(str(text), font_size=18).move_to(textPlacement)
           self.play(FadeIn(explanatoryText))
        
        if isAnimation:
            self.storedAnimations.append(FadeIn(pointer))
            firstIndexOfChange = min(rootParrentIndex,rootChildIndex)
            self.animateMovement(firstIndexOfChange)
        else:
            self.add(pointer)
            self.sceneUpToDate = False
            
        self.finish(isAnimation)

        if showExplanatoryText and isAnimation:
            self.play(FadeOut(explanatoryText))

    def delete(self, deleteDotID: int, isAnimation: bool):
        self.prepare(isAnimation)
        
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.get_root_index_from_key(self.root, deleteDotID)

        self.root.remove(deleteDot)
    
        childrenArrows = []
        if (len(deleteDot.children)>0):
            deleteDot.children.reverse()
            for n in deleteDot.children:
                childrenArrows.append(n.arrow)
                n.arrow = None
                n.parentKey = None
                self.root.append(n)

        self.nodeDic.pop(deleteDot.id)  #TODO No test if it works
        if isAnimation:
            for n in childrenArrows:
                self.storedAnimations.append(FadeOut(n))
            self.storedAnimations.append(FadeOut(deleteDot.dot))
            if self.showLabels:
                self.storedAnimations.append(FadeOut(deleteDot.numberLabel))
            self.animateMovement(index)
        else:
            if self.showLabels:
                self.remove(deleteDot.numberLabel)
            self.remove(deleteDot.dot)
            for n in childrenArrows:
                self.remove(n)
            self.sceneUpToDate = False

        self.finish(isAnimation)
        self.adjust_camera(isAnimation)
    
    def set_min(self, min_id, isAnimation):
        min_node_index = self.get_root_index_from_key(self.root, min_id)
        if not isinstance(min_node_index, int):
            return
        minFiboNode = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.dot.color = BLUE

        self.min_node = minFiboNode
        minFiboNode.dot.color = RED
        self.adjust_camera(isAnimation)

    def change_key(self, nodeId, newValue: int, isAnimation: bool, showExplanatoryText: bool=False):
        self.prepareSceneForAnimations(isAnimation)

        node = self.nodeDic[nodeId]
        new_text = Text(str(newValue), font_size=18 - (newValue/100)).move_to(node.dot.get_center()).set_z_index(1) #TODO why not just change the text???
        if showExplanatoryText:
            text = "Decrease key of node " + str(node.id) + " to " + str(newValue) #is it alway decrease????
            self.write_explanatory_text_to_video(text)
        if isAnimation:
            if self.showLabels:
                self.play(FadeOut(node.numberLabel), FadeIn(new_text))
            #self.play(Transform(node.numberLabel, new_text)) #more expensive? and leaves the other the screen
            node.numberLabel = new_text
        else:
            node.numberLabel.become(new_text)

    def cut(self, node_to_cut_ID: int, isAnimation: bool, unMark, showExplanatoryText: bool=False):
        self.prepare(isAnimation)
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

        firstIndexOfChange = 0
        root_parent = parent_node
        while True:
            if root_parent.parentKey is None:
                firstIndexOfChange = self.get_root_index_from_key(self.root, root_parent.id)
                break
            root_parent = self.nodeDic[root_parent.parentKey]

        if isAnimation:
            self.storedAnimations.append(FadeOut(arrowToBeRemoved))
            self.animateMovement(firstIndexOfChange)
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
        self.finish(isAnimation)
        
    def cascading_cut(self, decreased_node_parent_id, isAnimation, showExplanatoryText):
        self.prepare(isAnimation)
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


    ##########################################################################
    ################### Preformace functions based on size ###################
    def remove_label_check(self): #low quality: 35 dots - medium: ??- High: 65 dots - Production: 97 - 4k: 110 
        qualityNumber = 35
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
    

    ############################################################
    ################### Pre and Post Functions ###################
    def prepare(self, isAnimation: bool = True):
        if isAnimation and not self.sceneUpToDate:
            self.prepareSceneForAnimations()

    def finish(self, isAnimation: bool = True):
        self.remove_label_check()
        if isAnimation:
            self.buildAnimations(isAnimation)
            self.executeStoredAnimations()
    
    #############################################################
    ################### Tree Layout functions ###################
    def animateMovement(self, startIndex: int):
        if self.treeLayout == TreeLayout.RightAlligned:
            self.animate_root(startIndex)
        elif self.treeLayout == TreeLayout.Balanced:
            NotImplemented
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Animate(startIndex)

    def prepareSceneForAnimations(self):
        if self.treeLayout == TreeLayout.RightAlligned:
            self.build_scene(0)
        elif self.treeLayout == TreeLayout.Balanced:
            NotImplemented
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Build(0)

        self.sceneUpToDate = True
        self.adjust_camera(False)

    def changeTreeLayout(self, layout: TreeLayout = TreeLayout.RightAlligned, isAnimation: bool = False):
        if self.treeLayout == layout:
            return
        self.treeLayout = layout

        if not isAnimation:
            self.sceneUpToDate = False
            return
        
        if self.treeLayout == TreeLayout.RightAlligned:
            self.animate_root(0)
        elif self.treeLayout == TreeLayout.Balanced:
            NotImplemented
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Animate(0)

    def FOO():
        #something something width and heigth
        return
    def BAR(isanimation:bool = True):
        #something something move around
        return

    #############################################################################
    ################### Build animations and execute movement ###################
    def buildAnimations(self, isAnimation):
        listOfAnimations = list[Animation]()
        for n in self.mobjsTOmove:
            listOfAnimations.append(MoveToTarget(n.dot))
            if self.showLabels:
                listOfAnimations.append(n.numberLabel.animate.move_to(n.dot.target.get_center()))
            if not (n.arrow is None):
                listOfAnimations.append(n.arrow.animate.put_start_and_end_on(n.dot.target.get_center(), self.nodeDic[n.parentKey].dot.target.get_center()))
            
            #TODO should it be here??
            if n.dot.target.get_center()[0] > self.camera.frame.get_right()[0] or n.dot.target.get_center()[0] < self.camera.frame.get_left()[0]:
                self.adjust_camera(isAnimation) 
            if n.dot.target.get_bottom()[1] < self.camera.frame.get_bottom()[1]:
                self.bottom_node = n.dot.target
                self.adjust_camera(isAnimation)
                self.bottom_node = None
            n.target = None
        self.mobjsTOmove = list[self.FiboDot]()
        self.storedAnimations.extend(listOfAnimations)
        return 

    def executeStoredAnimations(self):
        self.play(*self.storedAnimations)
        self.storedAnimations = list[Animation]()
        return
    

    ##############################################
    ################### Camera ###################    
    def adjust_camera(self, isAnimation):
        self.prepare(isAnimation)
        mostLeftNode = self.get_left_most_dot(self.root)
        mostRightNode = self.root[len(self.root)-1]
        mostBottomDot = self.get_bottom_most_dot()

        #Do not adjust camera with a node that is in default add point
        if mostRightNode.dot.get_center()[1] == 3:
            return

        rightPoint = mostRightNode.dot.get_right()
        leftPoint = mostLeftNode.dot.get_left()

        newWidth = (rightPoint[0]-leftPoint[0])+2
        self.defaultAddPoint[0] = (rightPoint[0]+leftPoint[0])/2

        newHeight = 0
        if mostBottomDot is not None:
            top_point = self.camera.frame.get_top()[1]
            bottom_point = mostBottomDot.get_center()[1]
            newHeight = (top_point-bottom_point)+2

        newWidth = max(newWidth, newHeight*(self.width / self.height))
        
        boarderRight = self.camera.frame.get_right()[0]
        boarderLeft = self.camera.frame.get_left()[0]
        screenWidth = boarderRight-boarderLeft

        newCenter = (((rightPoint[0]+leftPoint[0])/2), self.camera.frame.get_y(), 0)

        if newWidth > screenWidth:
            self.zoom_out(isAnimation, newCenter, newWidth)
        elif newWidth > self.width and newWidth < screenWidth:
            self.zoom_in(isAnimation, newCenter, newWidth)
        else:
            if isAnimation:
                self.play(self.camera.frame.animate.move_to(newCenter))
            else:
                self.camera.frame.move_to(newCenter)

    def zoom_in(self, isAnimation, newCenter, currentWidthOfHeap):
        if isAnimation:
            self.play(self.camera.frame.animate.set_width(currentWidthOfHeap).move_to(newCenter))  
        else:
            self.camera.frame.set_width(currentWidthOfHeap).move_to(newCenter)         

    def zoom_out(self, isAnimation, newCenter, currentWidthOfHeap):
        if isAnimation:
            self.play(self.camera.frame.animate.set_width(currentWidthOfHeap).move_to(newCenter))  
        else:
            self.camera.frame.set_width(currentWidthOfHeap).move_to(newCenter) 


    ######################################################
    ################### Util Functions ###################
    def get_root_index_from_key(self, root: list, key: int):
        for n in range(len(root)):
            a = root[n]
            if a.id == key:
                return n
        return -1

    def get_left_most_dot(self, group: list[FiboDot]): #TODO only works on some layouts?
        if len(group) == 0:
            return #TODO should it return something to tell it failed??
        
        def aux(a: self.FiboDot):
            if len(a.children) > 0:
                return aux(a.children[len(a.children)-1])
            else:
                return a
        
        return aux(group[0])
    
    def get_bottom_most_dot(self):
        return self.bottom_node


    ##########################################################################
    ################### Allign with parent right - Layout. ###################
    def space_list_dots_by_tree_width(self, lst: list[FiboDot], isToTarget: bool = False, direction: Vector3 = LEFT, **kwargs):
        if isToTarget:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        else:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.next_to(m1.dot, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        return lst
    
    def update_widthOfChildren(self, parent: FiboDot, child: FiboDot, isAddingNode: bool):
        if isAddingNode:
            gainedWidth = int() 
            if len(parent.children) == 1:
                gainedWidth = 0
            else:
                gainedWidth = child.widthOfChildren + parent.dot.radius*4
            parent.widthOfChildren = parent.widthOfChildren + gainedWidth
        else:
            #If we remove a child in the middle of a tree, the tree should "move together" and become more narrow
            Temp_node = parent
            while isinstance(Temp_node, self.FiboDot):
                Temp_node.widthOfChildren = Temp_node.widthOfChildren - child.widthOfChildren
                Temp_node = self.nodeDic.get(Temp_node.parentKey)            
    
    def animate_root(self, startIndex: int): #Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends.
        if startIndex >= len(self.root): #this can happen if the last dot in root is removed
            return

        def aux (rootIndex: int, lastDotDestination: Point3D):
            if rootIndex == len(self.root):
                return
            currentDot = self.root[rootIndex]
            if not isinstance(currentDot, self.FiboDot): #TODO why is this still needed?
                return 
            currentDot.dot.target = Dot(point=currentDot.dot.get_center(), radius=currentDot.dot.radius, color=currentDot.dot.color)
            currentDot.dot.target.set_x(lastDotDestination[0]+currentDot.widthOfChildren+currentDot.dot.radius*4).set_y(lastDotDestination[1])
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
            currentDot.dot.set_x(lastDotDestination.get_x()+currentDot.widthOfChildren+currentDot.dot.radius*4).set_y(lastDotDestination.get_y())
            
            if self.showLabels:
                currentDot.numberLabel.move_to(currentDot.dot.get_center())

            self.move_children(currentDot)
            
            aux(root, rootIndex+1, currentDot.dot)

        aux(self.root, startIndex, self.root[startIndex-1].dot)
        return
        
    def move_children(self, parentMojb: FiboDot):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        parentMojb.children[0].dot.set_y(parentMojb.dot.get_y()-1.5).align_to(parentMojb.dot, RIGHT)
        
        #Arrange rest based on first
        self.space_list_dots_by_tree_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)
            self.move_children(n)


    ###############################################
    ################### HV-Tree ###################
    def hv_Tree_screen_placement():
        NotImplemented
    
    def hv_Tree_Animate(self, startIndex: int):
        if startIndex >= len(self.root): #TODO is this needed in the function
            return

        startFDot = self.root[startIndex]

        standardDistance = startFDot.dot.radius*4
        ba = self.transformToBinary(startFDot)
        maxIndex = len(ba)

        isLeftIsClosest_ = (len(startFDot.children)%2==0)

        def aux(i: int, isLeftIsClosest: bool, x: float, y: float):
            currentDot = ba[i]
            if not isinstance(currentDot, self.FiboDot):
                return
            
            currentDot.dot.target = Dot(point=(currentDot.dot.get_center()), radius=currentDot.dot.radius, color=currentDot.dot.color)
            currentDot.dot.target.set_x(x).set_y(y)
            if currentDot.id != -1:
                self.mobjsTOmove.append(currentDot)

            if i*2+2>=maxIndex:
                return

            left = ba[i*2+1]
            leftH = 0
            if left is not None:
                leftH = left.widthOfChildren

            rigth = ba[i*2+2]
            rigthV = 0
            if rigth is not None:
                rigthV = rigth.heigthOfChildren
    

            leftY= 0.0; rightX = 0.0
            dt = currentDot.dot.target

            if isLeftIsClosest:
                leftY = dt.get_y()-standardDistance
                rightX = dt.get_x()+leftH+standardDistance
            else:
                leftY = dt.get_y()-rigthV-standardDistance
                rightX = dt.get_x()+standardDistance
                
            rightY = dt.get_y()
            leftX = dt.get_x()

            aux(i*2+1, (not isLeftIsClosest), leftX, leftY)
            aux(i*2+2, (not isLeftIsClosest), rightX, rightY)

        aux(0, isLeftIsClosest_, startFDot.dot.get_x(), startFDot.dot.get_y())
        return   

    def hv_Tree_Build(self, startIndex: int):
        if startIndex >= len(self.root): #TODO is this needed in the function
            return

        def aux(i: int, isLeftIsClosest: bool, x: float, y: float):
            currentDot = ba[i]
            if not isinstance(currentDot, self.FiboDot):
                return

            currentDot.dot.move_to((x,y,0))
            if self.showLabels and currentDot.id != -1:
                currentDot.numberLabel.move_to(currentDot.dot.get_center())
            if currentDot.arrow is not None:
                currentDot.arrow.put_start_and_end_on(currentDot.dot.get_center(), self.nodeDic[currentDot.parentKey].dot.get_center())

            if i*2+2>=maxIndex:
                return

            left = ba[i*2+1]
            leftH = 0
            if left is not None:
                leftH = left.widthOfChildren

            rigth = ba[i*2+2]
            rigthV = 0
            if rigth is not None:
                rigthV = rigth.heigthOfChildren

            leftY= 0.0; rightX = 0.0
            dt = currentDot.dot

            if isLeftIsClosest:
                leftY = dt.get_y()-standardDistance
                rightX = dt.get_x()+leftH+standardDistance
            else:
                leftY = dt.get_y()-rigthV-standardDistance
                rightX = dt.get_x()+standardDistance
                
            rightY = dt.get_y()
            leftX = dt.get_x()

            aux(i*2+1, (not isLeftIsClosest), leftX, leftY)
            aux(i*2+2, (not isLeftIsClosest), rightX, rightY)


        for i in range((len(self.root)-startIndex)):
            startFDot = self.root[i]
            standardDistance = startFDot.dot.radius*4
            ba = self.transformToBinary(startFDot)
            maxIndex = len(ba)
            isLeftIsClosest_ = (len(startFDot.children)%2==0)
            aux(0, isLeftIsClosest_, startFDot.dot.get_x(), startFDot.dot.get_y())
        return 

    def transformToBinary(self, parrentDot: FiboDot):
        binaryArray = [None] * (int(len(self.nodeDic)*2*1.2)) #Make proof that there can be at max 20% fake nodes
        #TODO to much space of smaller trees...
        #: list[self.FiboDot]

        def aux(binaryIndex, fDot: self.FiboDot):
            binaryArray[binaryIndex] = fDot
            nChildren = len(fDot.children)            
            if nChildren == 0:
                return
            
            childN = nChildren
            aux(binaryIndex*2+2-childN%2, fDot.children[childN-1])#If even children place first left.

            childN -= 1
            currentIndex = binaryIndex*2+2-childN%2
            while childN >= 1:
                if childN == 1:
                    aux(currentIndex, fDot.children[0])
                    return

                fakeDot = self.FiboDot(-1)
                fakeDot.dot = Dot()
                binaryArray[currentIndex] = fakeDot

                aux(currentIndex*2+2-childN%2, fDot.children[childN-1])
                childN -= 1
                currentIndex = currentIndex*2+2-childN%2

        aux(0,parrentDot)
        self.updateDimentions(binaryArray, len(parrentDot.children)%2==0)
        return binaryArray

    def updateDimentions(self, binaryHeap: list[FiboDot], leftIsClosest: bool):    #NOT TAIL RECURSIVE!!!
        root = binaryHeap[0]
        distance = root.dot.radius*4
        maxIndex = len(binaryHeap)

        def updated(i: int, leftIsClosest_: bool):
            fDot = binaryHeap[i]
            if not isinstance(fDot, self.FiboDot):
                return 0,0

            fDot.widthOfChildren = 0
            fDot.heigthOfChildren = 0

            if i*2+2 >= maxIndex:
                return 0, 0
            
            leftHeigth = 0; leftWidth = 0
            if binaryHeap[i*2+1] is not None:
                leftHeigth, leftWidth = updated(i*2+1, (not leftIsClosest_))
                leftHeigth += distance

            rigthHeigth = 0; rigthWidth = 0
            if binaryHeap[i*2+2] is not None:
                rigthHeigth, rigthWidth = updated(i*2+2, (not leftIsClosest_))
                rigthWidth += distance

            if leftIsClosest_:
                fDot.widthOfChildren = rigthWidth+leftWidth
                fDot.heigthOfChildren = max(rigthHeigth, leftHeigth)
            else:
                fDot.widthOfChildren = max(leftWidth, rigthWidth)
                fDot.heigthOfChildren = rigthHeigth+leftHeigth
                
            return fDot.heigthOfChildren, fDot.widthOfChildren

        updated(0, leftIsClosest)

    def packingAlgorithmBL(self):
        class Rect:
            def __init__(self, height: int, width: int):
                self.x = None
                self.y = None
                self.h = height
                self.w = width
                self.placed = False

        rootBinaryTrees = list()
        rootRects = list()
        spacing = 0.8

        for i in self.root:
            rootBinaryTrees.append(self.transformToBinary(i))

        rootBinaryTrees.sort(key=lambda x: (x[0].heigthOfChildren,x[0].widthOfChildren), reverse=True)

        for i in rootBinaryTrees:
            rootRects.append(Rect(spacing+i[0].heigthOfChildren, spacing+i[0].widthOfChildren))

            

    #####################################################
    ################### Uncatagorized ###################