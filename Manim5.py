from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing_extensions import Self
from typing import TypedDict
import math
import time

#DO YOU HAVE TO STATE DELETIONS OF OBJECTS IN PYTHON TO HELP GARBAGE COLLECTER
#HOW DOES MANIM HANDLE REMOVED OBJECTS? ARE THEY DELTED?

ColorPalet = list(map(ManimColor, [(146,43,33), (231,76,60), (142,68,173), (155,89,182), (41,128,185), 
              (52,152,219), (20,90,50), (30,132,73), (39,174,96), (88,214,141),
              (211,84,0), (230,126,34), (243,156,18), (241,196,15)]))

class TreeLayout(Enum):
    RightAlligned = 1
    Balanced = 2
    TriangleBalanced = 3
    H_V = 4

class RootPacking(Enum):
    No_Packing = 1
    FFDH = 2
    Binary_Tree_Packing = 3

class RootSorting(Enum):
    Order = 1
    Heigth_Width = 2

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        #For node tree
        self.min_node: self.FiboDot = None
        self.root = list[self.FiboDot]()
        self.nodeDic = dict[int, self.FiboDot]()

        #For Animations and Display
        self.rootSpot = [0.0, 5.0, 0.0]
        self.defaultAddPoint = [0.0, 1.0, 0.0]
        self.treeLayout = TreeLayout(1)
        self.rootPacking = RootPacking(1)
        self.rootSorting = RootSorting(1)
        self.sceneUpToDate = True
        self.showLabels = True
        self.mobjsToMove = list()
        self.storedAnimations = list[Animation]()
        
        #Unique tree layout 
        self.treeVerticalSpacing = 1.5
        self.triangleLayer = 0
        self.rootDisplayOrder = list()
        self.rootBinaryTrees = list()
        self.triangels = dict[int, self.triangle]()
        self.showDepthColor = False #TODO implement
 
        #For Camera #TODO maybe the new rootPacking can create a current and new boundary
        self.bottom_node = None
        self.minimumheight = 7.993754879000781                                                                                                                                                                                              
        self.minimumwidth = 14.222222222222221
        self.multp = 0
        self.bounds = (0,0)
        self.newBounds = (0,0)


        self.rootRects = list() #TODO delete only for trouble shooting
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
        nFdotsInTree: int
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
            self.nFdotsInTree = 0
            self.widthOfChildren = 0
            self.heigthOfChildren = 0
            #self.arrow = Line()
            #self.numberLabel = Text("")


################################################################
################### Fibonacci Heap Functions ###################
    #Creates a FiboDot with a dot at "location", and numberLabel showing numberl, and return it without adding it to scene.
    def create_dot(self, point: Point3D, number: int, id: int):
        fiboDot = self.FiboDot(id)
        fiboDot.dot = Dot(point, radius=0.2, color=BLUE)
        fiboDot.numberLabel = Text(str(number), font_size=max(1,18 - (number/100))).move_to(fiboDot.dot.get_center()).set_z_index(1)
        return fiboDot

    #Inserts the dot onto the scene and adds it to a root list, then calls for a repositioning of the nodes.
    def insert_dot(self, number: int, isAnimation: bool, id: int):
        self.prepare(isAnimation)

        fiboDot = self.create_dot(self.defaultAddPoint, number, id)
        
        self.nodeDic[id] = fiboDot
        self.root.append(fiboDot)
        self.rootDisplayOrder.append(fiboDot)
        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees.append(self.transformToBinary(fiboDot))

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

        if isAnimation:
            self.animateTrees((len(self.root)-1))
        else:
            self.sceneUpToDate = False
        
        self.finish(isAnimation)

    def create_child(self, parentKey: int, childKey: int, isAnimation: bool, showExplanatoryText: bool = False):
        self.prepare(isAnimation)

        #Finding parent and child
        parentMobj = self.nodeDic.get(parentKey)
        childMojb = self.nodeDic.get(childKey)
        childMojb.parentKey = parentKey
        
        #Adding child to parent and removing from root
        parentMobj.children.append(childMojb)
        #Calculation new widths.
        self.update_widthOfChildren(parentMobj, childMojb, isAddingNode=True)
        self.update_heigthOfChildren(parentMobj, childMojb, isAddingNode=True)
        parentMobj.nFdotsInTree += 1+childMojb.nFdotsInTree

        #Removeing child from rootobjects
        self.root.remove(childMojb)
        childDisplayIndex = self.getIndexForDisplay(childMojb)
        parenDisplayIndex = self.getIndexForDisplay(parentMobj)

        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees[parenDisplayIndex] = self.transformToBinary(parentMobj)
            del self.rootBinaryTrees[childDisplayIndex]
        self.rootDisplayOrder.remove(childMojb)

        #creating arrow
        pointer = Line(childMojb.dot,parentMobj.dot).set_z_index(-1)
        childMojb.arrow = pointer

        if showExplanatoryText and isAnimation:
           text = "Compare " + str(parentMobj.id) + " < " + str(childMojb.id) + " and move " + str(childMojb.id) + " as a child of " + str(parentMobj.id)
           textPlacement = [self.camera.frame.get_top()[0], self.camera.frame.get_top()[1]-1, 0]
           explanatoryText = Text(str(text), font_size=18).move_to(textPlacement)
           self.play(FadeIn(explanatoryText))
        
        if isAnimation:
            self.storedAnimations.append(FadeIn(pointer))
            firstIndexOfChange = min(parenDisplayIndex, childDisplayIndex)
            self.animateTrees(firstIndexOfChange)
        else:
            self.add(pointer)
            self.sceneUpToDate = False
            
        self.finish(isAnimation)

        if showExplanatoryText and isAnimation:
            self.play(FadeOut(explanatoryText))

    def delete(self, deleteDotID: int, isAnimation: bool):
        self.prepare(isAnimation)
        
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.getIndexForDisplay(deleteDot)

        self.root.remove(deleteDot)
        if self.treeLayout == TreeLayout.H_V:
            del self.rootBinaryTrees[index]
        self.rootDisplayOrder.remove(deleteDot)
    
        childrenArrows = []
        if (len(deleteDot.children)>0):
            deleteDot.children.reverse()
            for n in deleteDot.children:
                childrenArrows.append(n.arrow)
                n.arrow = None
                n.parentKey = None
                self.root.append(n)
                self.rootDisplayOrder.append(n)
                if self.treeLayout == TreeLayout.H_V:
                    self.rootBinaryTrees.append(self.transformToBinary(n))

        self.nodeDic.pop(deleteDot.id)  #TODO No test if it works
        if isAnimation:
            for n in childrenArrows:
                self.storedAnimations.append(FadeOut(n))
            self.storedAnimations.append(FadeOut(deleteDot.dot))
            if self.showLabels:
                self.storedAnimations.append(FadeOut(deleteDot.numberLabel))
            self.animateTrees(index)
        else:
            if self.showLabels:
                self.remove(deleteDot.numberLabel)
            self.remove(deleteDot.dot)
            for n in childrenArrows:
                self.remove(n)
            self.sceneUpToDate = False

        self.finish(isAnimation)
    
    def set_min(self, min_id):#, isAnimation):
        min_node_index = self.get_root_index_from_key(min_id)
        if not isinstance(min_node_index, int):
            return
        minFiboNode = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.dot.color = BLUE

        self.min_node = minFiboNode
        minFiboNode.dot.color = RED
        #self.adjust_camera(isAnimation) #why is this needed????

    def change_key(self, nodeId, newValue: int, isAnimation: bool, showExplanatoryText: bool=False):
        self.prepare(isAnimation)

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
        self.rootDisplayOrder.append(node_to_cut)
        
        self.update_widthOfChildren(parent_node, node_to_cut, isAddingNode=False)
        self.update_heigthOfChildren(parent_node, node_to_cut, isAddingNode=False)

        firstIndexOfChange = 0
        root_parent = parent_node
        while True:
            if root_parent.parentKey is None:
                firstIndexOfChange = self.getIndexForDisplay(root_parent)
                break
            root_parent = self.nodeDic[root_parent.parentKey]

        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees.append(self.transformToBinary(node_to_cut))
            self.rootBinaryTrees[firstIndexOfChange] = self.transformToBinary(root_parent)

        if isAnimation:
            self.storedAnimations.append(FadeOut(arrowToBeRemoved))
            self.animateTrees(firstIndexOfChange)
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
    

#############################################################################
################### Build animations and execute movement ###################
    def buildAnimations(self):
        listOfAnimations = list[Animation]()
        for n in self.mobjsToMove:
            if isinstance(n, self.FiboDot):
                listOfAnimations.append(MoveToTarget(n.dot))
                if self.showLabels:
                    listOfAnimations.append(n.numberLabel.animate.move_to(n.dot.target.get_center()))
                if not (n.arrow is None):
                    listOfAnimations.append(n.arrow.animate.put_start_and_end_on(n.dot.target.get_center(), self.nodeDic[n.parentKey].dot.target.get_center()))
                n.target = None
            elif isinstance(n, self.triangle):
                listOfAnimations.append(MoveToTarget(n.mobj))
                listOfAnimations.append(n.text.animate.move_to(self.mobj.target.get_center_of_mass(), UP))
        self.mobjsToMove = list()
        self.storedAnimations.extend(listOfAnimations)
        return 

    def executeStoredAnimations(self):
        self.play(*self.storedAnimations)
        self.bounds = self.newBounds
        self.storedAnimations = list[Animation]()
        return


############################################################
################### Pre and Post Functions ###################
    def prepare(self, isAnimation: bool = True):
        if isAnimation and not self.sceneUpToDate:
            self.buildTrees(0)
            self.sceneUpToDate = True
            self.adjust_camera(False)

    def finish(self, isAnimation: bool = True):
        self.remove_label_check()
        if isAnimation:
            self.buildAnimations()
            self.executeStoredAnimations()
            self.adjust_camera(True)


#############################################################
################### Tree Layout functions ###################
    def animateTrees(self, startIndex_: int):
        startIndex = self.updateStartIndex(startIndex_)
        if startIndex is None:
            return

        self.rootPackingAlgorithms(startIndex, True)

        if self.treeLayout == TreeLayout.RightAlligned:
            self.right_align_tree_animate(startIndex)
        elif self.treeLayout == TreeLayout.Balanced:
            self.balanced_tree_animate(startIndex)
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Animate(startIndex)

    def buildTrees(self, startIndex:int):
        self.rootPackingAlgorithms(startIndex, False)

        if self.treeLayout == TreeLayout.RightAlligned:
            self.right_align_tree_build(startIndex)
        elif self.treeLayout == TreeLayout.Balanced:
            self.balance_tree_build(startIndex)
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Build(0)

    def changeTreeLayout(self, layout: TreeLayout = TreeLayout.RightAlligned, isAnimation: bool = True, affectedLayer: int = 0):
        if self.treeLayout == layout:
            return

        if len(self.root)==0:
            self.treeLayout = layout
            return
            
        self.prepare(isAnimation)

        self.rootBinaryTrees = list()
        if layout == TreeLayout.H_V:
            for r in self.rootDisplayOrder:
                self.rootBinaryTrees.append(self.transformToBinary(r))
                
        if self.treeLayout == TreeLayout.H_V:
            for i in self.rootDisplayOrder:
                self.recalcTreeDimentions(i)
            for i in self.nodeDic.values():
                i.dot.color = BLUE

        if self.treeLayout == TreeLayout.TriangleBalanced:
            NotImplemented

        self.treeLayout = layout
        
        if not isAnimation:
            self.sceneUpToDate = False
            return 
        
        self.animateTrees(0)
        
        self.finish(isAnimation)


#####################################################
################### Root movement ###################
    def rootPackingAlgorithms(self, startIndex: int, isAnimation: bool):
        if startIndex < 0 or startIndex >= len(self.rootDisplayOrder) or len(self.root) == 0:
            return

        rootRects = self.createRettangels()

        resolution = (1920, 1080) #TODO should this be a field connected to quality???
        boundsY = rootRects[0].h
        boundsX = boundsY * (resolution[0]/resolution[1])
        if boundsX < rootRects[0].w:
            boundsX = rootRects[0].w
            boundsY = boundsX * (resolution[1]/resolution[0])

        if boundsX < self.minimumwidth:
            boundsX = self.minimumwidth
            boundsY = self.minimumheight

        placedAllRoots = False
        
        while not placedAllRoots:
            if self.rootPacking == RootPacking.No_Packing:
                placedAllRoots = self.noPacking(boundsX, boundsY, rootRects)
            elif self.rootPacking == RootPacking.FFDH:
                placedAllRoots = self.fFDH_Packing(boundsX, boundsY, rootRects)
            elif self.rootPacking == RootPacking.Binary_Tree_Packing:
                placedAllRoots = self.binary_Tree_Packing(boundsX, boundsY, rootRects)
            
            if not placedAllRoots:
                boundsY += boundsY*0.2
                boundsX += boundsX*0.2
        
        self.newBounds = (boundsX, boundsY)
        self.rootRects = rootRects #TODO delete only for trouble shooting (printing the squares)
        

        if isAnimation:
            if self.treeLayout == TreeLayout(1):
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    cDot = self.rootDisplayOrder[i+startIndex]
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x + rootRects[i+startIndex].w, rootRects[i+startIndex].y, 0), radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)   
            elif self.treeLayout == TreeLayout(2):
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    cDot = self.rootDisplayOrder[i+startIndex]
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x + (rootRects[i+startIndex].w/2), rootRects[i+startIndex].y, 0), radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)
            elif self.treeLayout == TreeLayout(3):
                for i in range(len(self.rootBinaryTrees)-startIndex): 
                    cDot = self.rootBinaryTrees[i+startIndex][0]
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x+self.rootDisplayOrder[0].dot.radius*4, rootRects[i+startIndex].y, 0), radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)
        else:
            if self.treeLayout == TreeLayout(1):
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    fDot = self.rootDisplayOrder[i+startIndex]
                    fDot.dot.move_to((rootRects[i+startIndex].x + rootRects[i+startIndex].w, rootRects[i+startIndex].y, 0))
                    if self.showLabels:
                        fDot.numberLabel.move_to(fDot.dot.get_center())
            elif self.treeLayout == TreeLayout(2):
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    fDot = self.rootDisplayOrder[i+startIndex]
                    fDot.dot.move_to((rootRects[i+startIndex].x + (rootRects[i+startIndex].w/2), rootRects[i+startIndex].y, 0))
                    if self.showLabels:
                        fDot.numberLabel.move_to(fDot.dot.get_center())
            elif self.treeLayout == TreeLayout(3): #StartIndex doesnt make sense when packing
                for i in range(len(self.rootBinaryTrees)): 
                    self.rootBinaryTrees[i][0].dot.move_to((rootRects[i].x+self.rootDisplayOrder[0].dot.radius*4, rootRects[i].y, 0))

    def sortRootsByWidthHeigth(self):
        if self.treeLayout == TreeLayout.RightAlligned or self.treeLayout == TreeLayout.Balanced:
            self.rootDisplayOrder.sort(key=lambda x: (x.heigthOfChildren, x.widthOfChildren), reverse=True) 
        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees.sort(key=lambda x: (x[0].heigthOfChildren, x[0].widthOfChildren), reverse=True) 
            newRootOrder = list()
            for x in self.rootBinaryTrees:
                newRootOrder.append(x[0])
            self.rootDisplayOrder = newRootOrder

    def getIndexForDisplay(self, fDot: FiboDot):
        x = 0
        for i in self.rootDisplayOrder:
            if fDot.id == i.id:
                return x
            x += 1
        return 0

    def changeRootPackingAndSorting(self, rootPacking: RootPacking = RootPacking.No_Packing, rootSorting: RootSorting = RootSorting.Order, isAnimation: bool = False):
        if rootPacking == self.rootPacking and rootSorting == self.rootSorting:
            return

        if rootPacking != self.rootPacking:
            self.rootPacking = rootPacking
        
        if rootSorting != self.rootSorting:
            self.rootSorting = rootSorting
            if self.rootSorting == RootSorting.Order:
                self.rootDisplayOrder = self.root.copy()
                if self.treeLayout == TreeLayout.H_V:
                    self.restoreOrderInBinaryRootList()
        
        if not isAnimation:
            self.sceneUpToDate = False
            return

        self.prepare(isAnimation)
        
        self.animateTrees(0)
        
        self.finish(isAnimation)

    def createRettangels(self):
        class Rect:
            def __init__(self, height: int, width: int):
                self.x = None
                self.y = None
                self.h = height
                self.w = width

        rootRects = list()
        spacing = self.rootDisplayOrder[0].dot.radius*4

        if self.treeLayout == TreeLayout(1):
            for r in self.rootDisplayOrder:
                rootRects.append(Rect(spacing+r.heigthOfChildren, spacing+r.widthOfChildren))
            # rootRects[0].x = self.rootDisplayOrder[0].dot.get_x()-(self.rootDisplayOrder[0].widthOfChildren)-spacing #If we want a non moving index 0
            # rootRects[0].y = self.rootDisplayOrder[0].dot.get_y()
            rootRects[0].x = 0#-(self.rootDisplayOrder[0].widthOfChildren)-spacing
            rootRects[0].y = 0
        elif self.treeLayout == TreeLayout(2):
            for r in self.rootDisplayOrder:
                rootRects.append(Rect(spacing+r.heigthOfChildren, spacing+r.widthOfChildren))
            rootRects[0].x = 0#-(self.rootDisplayOrder[0].widthOfChildren/2)-spacing
            rootRects[0].y = 0
        elif self.treeLayout == TreeLayout(3):
            for r in self.rootBinaryTrees:
                rootRects.append(Rect(spacing*2 + r[0].heigthOfChildren, spacing*2+r[0].widthOfChildren))
            rootRects[0].x = 0
            rootRects[0].y = 0

        return rootRects
        
    def updateStartIndex(self, startIndex_ :int):
        if startIndex_ < 0 or startIndex_ >= len(self.rootDisplayOrder) or len(self.root) == 0:
            return

        startIndex = startIndex_
        if self.rootPacking == RootPacking.Binary_Tree_Packing:
            if self.rootSorting == RootSorting.Heigth_Width:
                self.sortRootsByWidthHeigth()
            startIndex = 0
            return startIndex
        
        if self.rootSorting == RootSorting.Heigth_Width:
            NodeAtChange = self.rootDisplayOrder[startIndex]
            self.sortRootsByWidthHeigth()
            startIndex = self.getIndexForDisplay(NodeAtChange)

        return startIndex

##############################################################
################### Root Packing functions ###################
    def noPacking(self, boundX_: int, boundY_: int, listOfRects: list):
        xPos = listOfRects[0].x
        yPos = listOfRects[0].y
        boundX = boundX_ + xPos
        boundY = boundY_ + yPos
        for r in listOfRects:
            if (xPos+r.w)>boundX:
                return False
            if (yPos+r.h)>boundY:
                return False
            r.x = xPos 
            r.y = yPos
            xPos += r.w 
 
        return True

    def fFDH_Packing(self, boundX_: int, boundY_: int, listOfRects: list):
        #Only promissed preformance of if decreasing heigth. 
        startx = listOfRects[0].x
        xPos = startx
        yPos = -listOfRects[0].y
        boundX = boundX_ + xPos
        boundY = boundY_ + yPos
        LargestHInRow = 0
        for r in listOfRects:
            if (xPos+r.w) > boundX:
                yPos += LargestHInRow
                xPos = startx
                LargestHInRow = 0
                if (xPos+r.w) > boundX:
                    return False 
                
            
            if (yPos+r.h)>boundY:
                return False

            r.x = xPos
            r.y = -yPos
            xPos += r.w

            if (r.h > LargestHInRow):
                LargestHInRow = r.h

        return True

    def binary_Tree_Packing(self, boundX: int, boundY: int, listOfRects: list):
        #Breakes the order of roots even if self.rootSorting = RootSorting(Order) 
        #Implementation rewritten from: https://www.david-colson.com/2020/03/10/exploring-rect-packing.html
        class Node():
            def __init__(self, x_: int, y_: int, w_: int, h_: int):
                self.x = x_
                self.y = y_
                self.w = w_
                self.h = h_
        
        freeSpaceNodes = list() #TODO preformace is propperly better if not useing list
        freeSpaceNodes.append(Node(listOfRects[0].x, listOfRects[0].y, boundX, boundY))

        for r in listOfRects:
            done = False

            i = len(freeSpaceNodes)-1
            while i>=0 and not done: 
                node = freeSpaceNodes[i]
                if node.w >= r.w and node.h >= r.h: 
                    r.x = node.x
                    r.y = node.y

                    remainingWidth = node.w - r.w
                    remainingHeight = node.h - r.h

                    newSmallerNode = Node(0,0,0,0)
                    newLargerNode = Node(0,0,0,0)
                    if remainingHeight > remainingWidth:
                        newSmallerNode.x = node.x + r.w
                        newSmallerNode.y = node.y
                        newSmallerNode.w = remainingWidth
                        newSmallerNode.h = r.h

                        newLargerNode.x = node.x
                        newLargerNode.y = node.y - r.h
                        newLargerNode.w = node.w
                        newLargerNode.h = remainingHeight
                    else: 
                        newSmallerNode.x = node.x
                        newSmallerNode.y = node.y - r.h
                        newSmallerNode.w = r.w
                        newSmallerNode.h = remainingHeight

                        newLargerNode.x = node.x + r.w
                        newLargerNode.y = node.y
                        newLargerNode.w = remainingWidth
                        newLargerNode.h = node.h
                
                    freeSpaceNodes.remove(freeSpaceNodes[i])
                    freeSpaceNodes.append(newLargerNode)
                    freeSpaceNodes.append(newSmallerNode)

                    done = True
                i -= 1

            if not done:
                return False
        
        return True


##########################################################################
################### Allign with parent right - Layout. ###################
    def space_children_by_thier_own_width(self, lst: list[FiboDot], isToTarget: bool = False, direction: Vector3 = LEFT, **kwargs):
        if isToTarget:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        else:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.next_to(m1.dot, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        return lst
  
    def right_align_tree_animate(self, startIndex):#TODO Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends
        for i in range(len(self.rootDisplayOrder)-startIndex):
            x = self.rootDisplayOrder[i+startIndex]
            self.ra_create_children_animations(x, x.dot.target)

    def ra_create_children_animations(self, parentMojb: FiboDot, parentTarget: Dot):
        if len(parentMojb.children)==0:
            return

        #First child which the other children should be alinged left of
        baseChild = parentMojb.children[0]
        baseChild.dot.target = Dot(point=baseChild.dot.get_center(), radius=baseChild.dot.radius, color=baseChild.dot.color).set_y(parentTarget.get_y()-self.treeVerticalSpacing).align_to(parentTarget, RIGHT)
        self.mobjsToMove.append(baseChild)

        for i in range(len(parentMojb.children)-1):
            child =  parentMojb.children[i+1]
            child.dot.target = Dot(point=child.dot.get_center(), radius=child.dot.radius, color=child.dot.color)
            self.mobjsToMove.append(child)
        
        #Arrange based on first child.
        self.space_children_by_thier_own_width(parentMojb.children, True)

        for n in range(len(parentMojb.children)):
            self.ra_create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target)
        return
    
    def right_align_tree_build(self, startIndex: int):
        for i in range(len(self.rootDisplayOrder)-startIndex):
            self.ra_move_children(self.rootDisplayOrder[i+startIndex])

    def ra_move_children(self, parentMojb: FiboDot):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        parentMojb.children[0].dot.set_y(parentMojb.dot.get_y()-self.treeVerticalSpacing).align_to(parentMojb.dot, RIGHT)
        
        #Arrange rest based on first
        self.space_children_by_thier_own_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)
            self.ra_move_children(n)

    def recalcTreeDimentions(self, rootDot: FiboDot):    #TODO NOT TAIL RECURSIVE!!!
        distance = self.root[0].dot.radius*4

        def updated(fDot: self.FiboDot):
            if not isinstance(fDot, self.FiboDot):
                return #Error
            
            if len(fDot.children) == 0:
                fDot.widthOfChildren = 0 
                fDot.heigthOfChildren = 0
                return (0, 0)

            if len(fDot.children) == 1:
                fDot.widthOfChildren = 0
                fDot.heigthOfChildren = self.treeVerticalSpacing
                return (0, self.treeVerticalSpacing)
            
            width = 0
            heigth = 0
            for i in fDot.children:
                updated(i)
                width += i.widthOfChildren
                heigth = max(heigth, i.heigthOfChildren)
            fDot.widthOfChildren = width+distance*(len(fDot.children)-1)
            fDot.heigthOfChildren = heigth+self.treeVerticalSpacing
                
            return fDot.heigthOfChildren, fDot.widthOfChildren

        updated(rootDot)

###############################################
################### Balanced Trees ###################
            
    def space_children_by_halv_thier_width(self, lst: list[FiboDot], isToTarget: bool = False, direction: Vector3 = LEFT, **kwargs):
        if isToTarget:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren/2 + m2.widthOfChildren/2 + m1.dot.radius*2), **kwargs)
        else:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.next_to(m1.dot, direction, (m1.widthOfChildren/2 + m2.widthOfChildren/2 + m1.dot.radius*2), **kwargs)
        return lst

    def balanced_tree_animate(self, startIndex):#TODO Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends
        for i in range(len(self.rootDisplayOrder)-startIndex):
            x = self.rootDisplayOrder[i+startIndex]
            self.bal_create_children_animations(x, x.dot.target)

    def bal_create_children_animations(self, parentMojb: FiboDot, parentTarget: Dot):
        if len(parentMojb.children)==0:
            return

        #First child which the other children should be alinged left of
        baseChild = parentMojb.children[0]
        baseChild.dot.target = Dot(point=baseChild.dot.get_center(), radius=baseChild.dot.radius, color=baseChild.dot.color).set_y(parentTarget.get_y()-self.treeVerticalSpacing).set_x(parentTarget.get_x()+parentMojb.widthOfChildren/2-baseChild.widthOfChildren/2)
        self.mobjsToMove.append(baseChild)

        for i in range(len(parentMojb.children)-1):
            child =  parentMojb.children[i+1]
            child.dot.target = Dot(point=child.dot.get_center(), radius=child.dot.radius, color=child.dot.color)
            self.mobjsToMove.append(child)
        
        #Arrange based on first child.
        self.space_children_by_halv_thier_width(parentMojb.children, True)

        for n in range(len(parentMojb.children)):
            self.bal_create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target)
        return

    def balance_tree_build(self, startIndex: int):
        for i in range(len(self.rootDisplayOrder)-startIndex):
            self.bal_move_children(self.rootDisplayOrder[i+startIndex])

    def bal_move_children(self, parentMojb: FiboDot):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        parentMojb.children[0].dot.set_y(parentMojb.get_y()-self.treeVerticalSpacing).set_x(parentMojb.get_x()+parentMojb.widthOfChildren/2-parentMojb.children[0].widthOfChildren/2)
        
        #Arrange rest based on first
        self.space_children_by_halv_thier_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)
            self.bal_move_children(n)

#########################################################################################
################### Balanced Tree Extension - Triangle representation ###################

    def triangle_balanced_tree_animate(self, startIndex):#TODO Must be done smart. aka move the lesser tree. Or moving fixed distance if child is at the ends
        if self.triangleLayer == 0:
            for i in range(len(self.rootDisplayOrder)-startIndex):
                x = self.rootDisplayOrder[i+startIndex]
                self.removeChildrenFromScene(x)

                t = self.triangels.get(x.id)
                t.createTarget()
                self.mobjsToMove.remove(t.fDot)
                self.mobjsToMove.append(t.mobj)
            return
        else:
            for i in range(len(self.rootDisplayOrder)-startIndex):
                x = self.rootDisplayOrder[i+startIndex]
                self.tbal_create_children_animations(x, x.dot.target, 1)

    def tbal_create_children_animations(self, parentMojb: FiboDot, parentTarget: Dot, layer: int):
        if len(parentMojb.children)==0:
            return

        #First child which the other children should be alinged left of
        baseChild = parentMojb.children[0]
        baseChild.dot.target = Dot(point=baseChild.dot.get_center(), radius=baseChild.dot.radius, color=baseChild.dot.color).set_y(parentTarget.get_y()-self.treeVerticalSpacing).set_x(parentTarget.get_x()+parentMojb.widthOfChildren/2-baseChild.widthOfChildren/2)
        self.mobjsToMove.append(baseChild)

        for i in range(len(parentMojb.children)-1):
            child =  parentMojb.children[i+1]
            child.dot.target = Dot(point=child.dot.get_center(), radius=child.dot.radius, color=child.dot.color)
            self.mobjsToMove.append(child)
        
        #Arrange based on first child.
        self.space_children_by_halv_thier_width(parentMojb.children, True)

        if layer == self.triangleLayer:
            for x in parentMojb.children:
                self.removeChildrenFromScene(x)

                t = self.triangels.get(x.id)
                t.createTarget()
                self.mobjsToMove.remove(t.fDot)
                self.mobjsToMove.append(t.mobj)
            return

        for n in range(len(parentMojb.children)):
            self.bal_create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target, (layer+1))
        return

    def triangle_balance_tree_build(self, startIndex: int):
        if self.triangleLayer == 0:
            for i in range(len(self.rootDisplayOrder)-startIndex):
                x = self.rootDisplayOrder[i+startIndex]
                self.removeChildrenFromScene(x)

                t = self.triangels.get(x.id)
                t.move_to(x.dot.get_center(), UP)
                t.updateText()
            return
        for i in range(len(self.rootDisplayOrder)-startIndex):
            self.bal_move_children(self.rootDisplayOrder[i+startIndex], 1)

    def tbal_move_children(self, parentMojb: FiboDot, layer:int):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        parentMojb.children[0].dot.set_y(parentMojb.get_y()-self.treeVerticalSpacing).set_x(parentMojb.get_x()+parentMojb.widthOfChildren/2-parentMojb.children[0].widthOfChildren/2)
        
        #Arrange rest based on first
        self.space_children_by_halv_thier_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)

            if layer == self.triangleLayer:
                self.removeChildrenFromScene(n)

                t = self.triangels.get(n.id)
                t.createTarget()
                self.mobjsToMove.remove(t.fDot)
                self.mobjsToMove.append(t.mobj)
            else:
                self.bal_move_children(n, (layer+1))

    class triangle():
        def __init__(self, fDot, point: tuple[float, float, float]) -> None:
            self.mobj = Triangle().set_fill(BLUE, opacity=1).move_to(point, UP)
            self.mobj.height = 1.5
            self.fDot = fDot
            self.text = Text(str(f"n: {self.fDot.nFdotsInTree}")).scale_to_fit_width(self.mobj.width*0.65).move_to(self.mobj.get_center_of_mass(), UP)
        def updateText(self, scene: Scene):
            scene.remove(self.text)
            self.text = Text(str(f"n: {self.fDot.nFdotsInTree}")).scale_to_fit_width(self.mobj.width*0.65).move_to(self.mobj.get_center_of_mass(), UP)
            scene.add(self.text)
        def createTarget(self):
            self.mobj.target = Triangle().set_fill(BLUE, opacity=1).move_to(self.fDot.dot.target.get_center(), UP)

    def createTriangels(self, dotList: list[FiboDot]):
        if dotList is None or len(dotList) == 0:
            return

        for x in dotList:
            self.removeChildrenFromScene(x)
            t = self.triangle(x, x.dot.get_center())
            self.add(t.mobj, t.text)
            self.triangels.update(t.fDot.id, t)

    def removeChildrenFromScene(self, fDot: FiboDot):
        for x in fDot.children:
            self.removeDotFromScene(x)
            self.removeChildrenFromScene(x)

    def removeDotFromScene(self, fDot: FiboDot):
        if fDot is None:
            return
        
        self.remove(fDot.dot)
        if fDot.parentKey is not None:
            self.remove(fDot.arrow)
        if self.showLabels:
            self.remove(fDot.numberLabel)
  
    def addChildrenToScene(self, fDot: FiboDot):
        if fDot is None:
            return
        
        for x in fDot.children:
            self.addDotToScene(x)
            self.addChildrenToScene(x)
    
    def addDotToScene(self, fDot: FiboDot):
        if fDot is None:
            return
        
        self.add(fDot.dot)
        if fDot.parentKey is not None:
            self.add(fDot.arrow)
        if self.showLabels:
            self.add(fDot.numberLabel)

###############################################
################### HV-Tree ###################
    def hv_Tree_Animate(self, startIndex: int):
        if startIndex < 0 or startIndex >= len(self.rootDisplayOrder):
            return

        def aux(i: int, isLeftIsClosest: bool, x: float, y: float, depth_: int):
            currentDot = ba[i]
            if not isinstance(currentDot, self.FiboDot):
                return
            
            depth = depth_

            currentDot.dot.target = Dot(point=(currentDot.dot.get_center()), radius=currentDot.dot.radius, color=self.getColorFromDepth(depth))
            currentDot.dot.target.set_x(x).set_y(y)
            if currentDot.id != -1:
                depth += 1
                self.mobjsToMove.append(currentDot)

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

            aux(i*2+1, (not isLeftIsClosest), leftX, leftY, depth)
            aux(i*2+2, (not isLeftIsClosest), rightX, rightY, depth)

        for i in range((len(self.rootDisplayOrder))-startIndex):
            fDot = self.rootDisplayOrder[i+startIndex]
            if len(fDot.children) == 0:
                continue
            standardDistance = fDot.dot.radius*4
            ba = self.rootBinaryTrees[i+startIndex]
            if ba[2] == None and ba[1] == None: # if the tree have changed.
                self.rootBinaryTrees[i+startIndex] = self.transformToBinary(fDot) 
                ba = self.rootBinaryTrees[i+startIndex]
            maxIndex = len(ba)
            isLeftIsClosest_ = (len(fDot.children)%2==0)
            targetX = fDot.dot.get_x()
            targetY = fDot.dot.get_y()
            if fDot.dot.target is not None:
                targetX = fDot.dot.target.get_x()
                targetY = fDot.dot.target.get_y()
            aux(0, isLeftIsClosest_, targetX, targetY, 0)

        return   

    def hv_Tree_Build(self, startIndex: int):
        if startIndex < 0 or startIndex >= len(self.rootDisplayOrder):
            return

        def aux(i: int, isLeftIsClosest: bool, x: float, y: float, depth_: int):
            currentDot = ba[i]
            if not isinstance(currentDot, self.FiboDot):
                return

            depth = depth_

            currentDot.dot.move_to((x,y,0))
            if self.showLabels and currentDot.id != -1:
                currentDot.numberLabel.move_to(currentDot.dot.get_center())
            if currentDot.arrow is not None:
                currentDot.arrow.put_start_and_end_on(currentDot.dot.get_center(), self.nodeDic[currentDot.parentKey].dot.get_center())
            currentDot.dot.color = self.getColorFromDepth(depth)

            if currentDot.id != -1:
                depth += 1

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

            aux(i*2+1, (not isLeftIsClosest), leftX, leftY, depth)
            aux(i*2+2, (not isLeftIsClosest), rightX, rightY, depth)


        for i in range((len(self.rootDisplayOrder)-startIndex)):
            fDot = self.rootDisplayOrder[i+startIndex]
            standardDistance = fDot.dot.radius*4
            ba = self.rootBinaryTrees[i+startIndex]
            if len(fDot.children) > 0 and ba[2] == None and ba[1] == None:
                ba = self.transformToBinary(fDot) 
            maxIndex = len(ba)
            isLeftIsClosest_ = (len(fDot.children)%2==0)
            aux(0, isLeftIsClosest_, fDot.dot.get_x(), fDot.dot.get_y(), 0)
        
        return 

    def transformToBinary(self, parrentDot: FiboDot):
        binaryArray = [None] * (int(len(self.nodeDic)*2*1.2)) #Make proof that there can be at max 20% fake nodes
        #TODO to much space of smaller trees... FIX with nDotsInTreeField. Also used in triangle 

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
        self.recalcBinaryTreeDimentions(binaryArray, len(parrentDot.children)%2==0)
        return binaryArray

    def recalcBinaryTreeDimentions(self, binaryHeap: list[FiboDot], leftIsClosest: bool):    #TODO NOT TAIL RECURSIVE!!!
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

    def restoreOrderInBinaryRootList(self):
        newBinRoot = list ()
        for i in self.rootDisplayOrder:
            for x in self.rootBinaryTrees:
                if x[0].id == i.id:
                    newBinRoot.append(x)
                    break
        self.rootBinaryTrees = newBinRoot

    def getColorFromDepth(self, depth: int):
        if depth < 0:
            return
        if depth > 13: 
            return ColorPalet[13]
        
        return ColorPalet[depth]

##############################################
################### Camera ###################    
    def adjust_camera(self, isAnimation):
        if len(self.rootDisplayOrder) < 1:
            return

        self.prepare(isAnimation)

        mostLeftX = self.get_left_most_dot(self.rootDisplayOrder).dot.get_x()
        xbound = self.newBounds[0]
        ybound = self.newBounds[1]
        
        boarderRight = self.camera.frame.get_right()[0]
        boarderLeft = self.camera.frame.get_left()[0]
        screenWidth = boarderRight-boarderLeft

        newCenter = (((mostLeftX+xbound)/2), 2+((self.rootDisplayOrder[0].dot.get_y()-ybound)/2), 0) #the +2 is a top padding

        newWidth = xbound+2
        if newWidth > screenWidth:
            self.zoom_out(isAnimation, newCenter, newWidth)
        elif newWidth > self.minimumwidth and newWidth < screenWidth:
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
    def update_heigthOfChildren(self, parent: FiboDot, child: FiboDot, isAddingNode: bool): 
        if self.treeLayout == TreeLayout.H_V:
            return
        if isAddingNode: 
            newHeigth = child.heigthOfChildren+self.treeVerticalSpacing
            if parent.heigthOfChildren < newHeigth:
                parent.heigthOfChildren = newHeigth
        else:
            if len(parent.children) == 0:
                parent.heigthOfChildren = 0
            else:
                hightOfTallestChild = 0
                for c in parent.children:
                    if c.heigthOfChildren > hightOfTallestChild:
                        hightOfTallestChild = c.heigthOfChildren
                parent.heigthOfChildren = hightOfTallestChild + self.treeVerticalSpacing

    def update_widthOfChildren(self, parent: FiboDot, child: FiboDot, isAddingNode: bool):
        if self.treeLayout == TreeLayout.H_V:
            return
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
                width = 0
                for i in Temp_node.children:
                    width += i.widthOfChildren
                Temp_node.widthOfChildren = max(0, width+(Temp_node.dot.radius*4)*(len(Temp_node.children)-1))
                Temp_node = self.nodeDic.get(Temp_node.parentKey)            
  

    def get_root_index_from_key(self, key: int):
        for n in range(len(self.root)):
            a = self.root[n]
            if a.id == key:
                return n
        return -1

    def get_left_most_dot(self, group: list[FiboDot]): 
        if len(group) == 0:
            return #TODO should it return something to tell it failed??
        
        if self.treeLayout == TreeLayout.H_V:
            return group[0]
        
        def aux(a: self.FiboDot):
            if len(a.children) > 0:
                return aux(a.children[len(a.children)-1])
            else:
                return a
        
        return aux(group[0])
    
    def get_bottom_most_dot(self): #TODO is it laysensitive? Is it needed?
        return self.bottom_node


#####################################################
################### Uncatagorized ###################