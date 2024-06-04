from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
from typing_extensions import Self
from typing import TypedDict
from layouts import *
import math



class TreeLayout(Enum):
    RightAlligned = 1
    Centered = 2
    H_V = 3

class RootPacking(Enum):
    horizontalPacking = 1
    FFDH = 2
    binaryTreePacking = 3

class RootSorting(Enum):
    Order = 1
    HeightWidth = 2

#New Scene class with a dictonary of keys and newdot pointers
class FiboScene(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        #For node tree
        self.min_node: self.FiboNode = None
        self.root = list[self.FiboNode]()
        self.nodeDic = dict[int, self.FiboNode]()

        #For Animations and Display
        self.defaultAddPoint = [0.0, 1.0, 0.0]
        self.treeLayout = Layout_Interface #TreeLayout(1)
        self.rootPacking = RootPacking(1)
        self.rootSorting = RootSorting(1)
        self.sceneUpToDate = True
        self.showLabels = True
        self.mobjsToMove = list()
        self.storedAnimations = list[Animation]()
        
        #Unique tree layout 
        self.treeVerticalSpacing = 1.5
        self.rootDisplayOrder = list()
        self.rootBinaryTrees = list()
        self.showDepthColor = False
 
        #For Camera 
        self.topMargin = 0
        self.minimumheight = 7.993754879000781                                                                                                                                                                                              
        self.minimumwidth = 14.222222222222221
        self.scalePercentage = 0.75
        self.bounds = (14.222222222222221,7.993754879000781)
        self.newBounds = (self.bounds[0], self.bounds[1]*self.scalePercentage)

        self.rootRects = list()
        super().__init__(*args, **kwargs)
        self.adjust_camera(False)
    
    def construct(self):
        self.wait(1)
        self.clear()

    #New class. Contains an ID and a parrentKey for the fibonacci heap to indenfify and modify individual instanses. 
        #Contains a manim dot, line and text. All needed for manim to display a node.
        #Contains a list of children, width and height of them. For calculating mobjects target location.
    class FiboNode:
        id: int
        parentKey: int
        children: list[Self]
        nFdotsInTree: int
        widthOfChildren: int
        heightOfChildren: int
        dot: Dot
        arrow: Line = None
        numberLabel: Text
        def __init__(self, idKey: int):
            self.id = idKey
            self.parentKey = None
            self.children = list[Self]()
            self.nFdotsInTree = 0
            self.widthOfChildren = 0
            self.heightOfChildren = 0
            self.marked = False

################################################################
################### Fibonacci Heap Functions ###################
    #Creates a FiboDot with a dot at "location", and numberLabel showing numberl, and return it without adding it to scene.
    def create_dot(self, point: Point3D, number: int, id: int):
        fiboDot = self.FiboNode(id)
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
            self.rootBinaryTrees.append(self.transform_to_binary(fiboDot))

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
            self.animate_trees((len(self.root)-1))
        else:
            self.sceneUpToDate = False
        
        self.finish(isAnimation)

    def create_child(self, parentKey: int, childKey: int, isAnimation: bool):
        self.prepare(isAnimation)

        #Finding parent and child
        parentMobj = self.nodeDic.get(parentKey)
        childMojb = self.nodeDic.get(childKey)
        childMojb.parentKey = parentKey
        
        #Adding child to parent and removing from root
        parentMobj.children.append(childMojb)
        #Calculation new widths.
        self.update_width_of_children(parentMobj, childMojb, isAddingNode=True)
        self.update_height_of_children(parentMobj, childMojb, isAddingNode=True)
        parentMobj.nFdotsInTree += 1+childMojb.nFdotsInTree

        #Removeing child from rootobjects
        self.root.remove(childMojb)
        childDisplayIndex = self.get_index_for_display(childMojb)
        parenDisplayIndex = self.get_index_for_display(parentMobj)

        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees[parenDisplayIndex] = self.transform_to_binary(parentMobj)
            del self.rootBinaryTrees[childDisplayIndex]
        self.rootDisplayOrder.remove(childMojb)

        #creating arrow
        pointer = Line(childMojb.dot,parentMobj.dot).set_z_index(-1)
        childMojb.arrow = pointer
        
        if isAnimation:
            self.storedAnimations.append(FadeIn(pointer))
            firstIndexOfChange = min(parenDisplayIndex, childDisplayIndex)
            self.animate_trees(firstIndexOfChange)
        else:
            self.add(pointer)
            self.sceneUpToDate = False
        
        self.finish(isAnimation)


    def delete(self, deleteDotID: int, isAnimation: bool):
        self.prepare(isAnimation)
        
        deleteDot = self.nodeDic.get(deleteDotID)
        index = self.get_index_for_display(deleteDot)

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
                    self.rootBinaryTrees.append(self.transform_to_binary(n))

        self.nodeDic.pop(deleteDot.id)
        if isAnimation:
            for n in childrenArrows:
                self.storedAnimations.append(FadeOut(n))
            self.storedAnimations.append(FadeOut(deleteDot.dot))
            if self.showLabels:
                self.storedAnimations.append(FadeOut(deleteDot.numberLabel))
            self.animate_trees(index)
        else:
            if self.showLabels:
                self.remove(deleteDot.numberLabel)
            self.remove(deleteDot.dot)
            for n in childrenArrows:
                self.remove(n)
            self.sceneUpToDate = False

        self.finish(isAnimation)
        for n in deleteDot.children:
            if n.dot.color != BLUE:
                if isAnimation:
                    self.play(n.dot.animate.set_color(BLUE))
                else:
                    n.dot.color = BLUE
    
    def set_min(self, minId):
        min_node_index = self.get_root_index_from_key(minId)
        if not isinstance(min_node_index, int):
            return
        minFiboNode = self.root[min_node_index]
        if self.min_node is not None:
            self.min_node.dot.color = BLUE

        self.min_node = minFiboNode
        minFiboNode.dot.color = RED 

    def change_key(self, nodeId, newValue: int, isAnimation: bool):
        self.prepare(isAnimation)
        text_size = newValue if isinstance(newValue,int) else 4
        node = self.nodeDic[nodeId]
        new_text = Text(str(newValue), font_size=18 - (text_size/100)).move_to(node.dot.get_center()).set_z_index(1)
        if isAnimation:
            if self.showLabels:
                self.play(FadeOut(node.numberLabel), FadeIn(new_text))
            node.numberLabel = new_text
        else:
            node.numberLabel.become(new_text)

    def cut(self, nodeToCutID: int, isAnimation: bool, unMark): 
        self.prepare(isAnimation)
        node_to_cut = self.nodeDic[nodeToCutID]
        parent_node = self.nodeDic[node_to_cut.parentKey]
        arrowToBeRemoved = node_to_cut.arrow
        node_to_cut.arrow = None
        node_to_cut.parentKey = None
        parent_node.children.remove(node_to_cut)
        self.root.append(node_to_cut)
        self.rootDisplayOrder.append(node_to_cut)
        
        self.update_width_of_children(parent_node, node_to_cut, isAddingNode=False)
        self.update_height_of_children(parent_node, node_to_cut, isAddingNode=False)

        firstIndexOfChange = 0
        rootParent = parent_node
        while True:
            if rootParent.parentKey is None:
                firstIndexOfChange = self.get_index_for_display(rootParent)
                break
            rootParent = self.nodeDic[rootParent.parentKey]

        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees.append(self.transform_to_binary(node_to_cut))
            self.rootBinaryTrees[firstIndexOfChange] = self.transform_to_binary(rootParent)

        if isAnimation:
            self.storedAnimations.append(FadeOut(arrowToBeRemoved))
            self.animate_trees(firstIndexOfChange)
        else:
            self.remove(arrowToBeRemoved)
            self.sceneUpToDate = False

        self.finish(isAnimation)

        if unMark:
            node_to_cut.marked = False
            if isAnimation:
                self.play(node_to_cut.dot.animate.set_color(BLUE))
            else:
                node_to_cut.dot.color = BLUE
        else: 
            node_to_cut.dot.color = BLUE
        
    def cascading_cut(self, decreased_node_parent_id, isAnimation):
        self.prepare(isAnimation)
        node = self.nodeDic[decreased_node_parent_id]
        node.marked = True
        if isAnimation:
            self.play(node.dot.animate.set_color(ORANGE))
        else:
            node.dot.color = ORANGE


##########################################################################
################### Preformace functions based on size ###################
    def remove_label_check(self): #low quality: 35 dots - medium: ??- High: 65 dots - Production: 97 - 4k: 110 
        qualityNumber = 300
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
    def build_animations(self):
        listOfAnimations = list[Animation]()
        for n in self.mobjsToMove:
            if isinstance(n, self.FiboNode):
                listOfAnimations.append(MoveToTarget(n.dot))
                if self.showLabels:
                    listOfAnimations.append(n.numberLabel.animate.move_to(n.dot.target.get_center()))
                if not (n.arrow is None):
                    listOfAnimations.append(n.arrow.animate.put_start_and_end_on(n.dot.target.get_center(), self.nodeDic[n.parentKey].dot.target.get_center()))
                n.target = None
        self.mobjsToMove = list()
        self.storedAnimations.extend(listOfAnimations)
        return 

    def execute_stored_animations(self):
        self.play(*self.storedAnimations)
        self.storedAnimations = list[Animation]()
        return

############################################################
################### Pre and Post Functions ###################
    def prepare(self, isAnimation: bool = True):
        if isAnimation and not self.sceneUpToDate:
            self.build_trees(0)
            self.sceneUpToDate = True
            self.adjust_camera(isAnimation=False)

    def finish(self, isAnimation: bool = True):
        self.remove_label_check()
        if isAnimation:
            self.build_animations()
            
            #Zoom out
            if self.newBounds[0] > self.bounds[0]:
                self.adjust_camera(isAnimation)
                self.bounds = self.newBounds

            self.execute_stored_animations()

            #Zoom in 
            if self.newBounds[0] < self.bounds[0]:
                self.adjust_camera(isAnimation)
                self.bounds = self.newBounds
        else:
            self.adjust_camera(isAnimation)
#############################################################
################### Tree Layout functions ###################
    def animate_trees(self, startIndex_: int):
        startIndex = self.update_start_index(startIndex_)
        if startIndex is None:
            return

        self.root_packing_algorithms(startIndex, True)

        if self.treeLayout == TreeLayout.RightAlligned:
            self.right_align_tree_animate(startIndex)
        elif self.treeLayout == TreeLayout.Centered:
            self.centered_tree_animate(startIndex)
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Animate(startIndex)

    def build_trees(self, startIndex:int):
        self.root_packing_algorithms(startIndex, False)

        if self.treeLayout == TreeLayout.RightAlligned:
            self.right_align_tree_build(startIndex)
        elif self.treeLayout == TreeLayout.Centered:
            self.centered_tree_build(startIndex)
        elif self.treeLayout == TreeLayout.H_V:
            self.hv_Tree_Build(0)

    def change_tree_layout(self, layout: TreeLayout = TreeLayout.RightAlligned, isAnimation: bool = True, showColorDepth: bool = False):
        if self.treeLayout == layout and self.showDepthColor == showColorDepth:
            return

        if len(self.root)==0:
            self.treeLayout = layout
            return
            
        self.prepare(isAnimation)

        self.rootBinaryTrees = list()
        if layout == TreeLayout.H_V:
            for r in self.rootDisplayOrder:
                self.rootBinaryTrees.append(self.transform_to_binary(r))
                
        if self.treeLayout == TreeLayout.H_V and layout != TreeLayout.H_V:
            for i in self.rootDisplayOrder:
                self.recalculate_tree_dimensions(i)

        self.treeLayout = layout
        
        if not isAnimation:
            self.sceneUpToDate = False
            return 
        
        if self.showDepthColor != showColorDepth:
            if not showColorDepth:
                self.restore_normal_color()
            self.showDepthColor = showColorDepth

        self.animate_trees(0)
        
        self.finish(isAnimation)


#####################################################
################### Root movement ###################
    def root_packing_algorithms(self, startIndex: int, isAnimation: bool):
        if startIndex < 0 or startIndex >= len(self.rootDisplayOrder) or len(self.root) == 0:
            return

        rootRects = self.create_rectangles()

        resolution = (1920, 1080)
        boundsY = rootRects[0].h
        boundsX = boundsY * (resolution[0]/resolution[1])
        if boundsX < rootRects[0].w:
            boundsX = rootRects[0].w
            boundsY = boundsX * (resolution[1]/resolution[0])

        if boundsX < self.minimumwidth:
            boundsX = self.minimumwidth
            boundsY = self.minimumheight

        boundsY = boundsY*self.scalePercentage
        placedAllRoots = False
        
        while not placedAllRoots:
            if self.rootPacking == RootPacking.horizontalPacking:
                placedAllRoots = self.horizontalPacking(boundsX, boundsY, rootRects)
            elif self.rootPacking == RootPacking.FFDH:
                placedAllRoots = self.nfdh_packing(boundsX, boundsY, rootRects)
            elif self.rootPacking == RootPacking.binaryTreePacking:
                placedAllRoots = self.binaryTreePacking(boundsX, boundsY, rootRects)
            
            if not placedAllRoots:
                boundsY += boundsY*0.2
                boundsX += boundsX*0.2

        if isAnimation:
            self.newBounds = (boundsX, boundsY)
        else:
            self.bounds = (boundsX, boundsY)

        self.rootRects = rootRects 

        if isAnimation:
            if self.treeLayout == TreeLayout.RightAlligned:
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    cDot = self.rootDisplayOrder[i+startIndex]
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x + rootRects[i+startIndex].w, rootRects[i+startIndex].y, 0), 
                                          radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)   
            elif self.treeLayout == TreeLayout.Centered:
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    cDot = self.rootDisplayOrder[i+startIndex]
                    widthOfLeftMostChild = 0
                    if len(cDot.children)>0:
                        widthOfLeftMostChild = cDot.children[-1].widthOfChildren              
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x + rootRects[i+startIndex].w/2 + widthOfLeftMostChild/4, 
                                                 rootRects[i+startIndex].y, 0), radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)
            elif self.treeLayout == TreeLayout.H_V:
                for i in range(len(self.rootBinaryTrees)-startIndex): 
                    cDot = self.rootBinaryTrees[i+startIndex][0]
                    cDot.dot.target = Dot(point=(rootRects[i+startIndex].x+self.rootDisplayOrder[0].dot.radius*4, 
                                                 rootRects[i+startIndex].y, 0), radius=cDot.dot.radius, color=cDot.dot.color)
                    self.mobjsToMove.append(cDot)
        else:
            if self.treeLayout == TreeLayout.RightAlligned:
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    fDot = self.rootDisplayOrder[i+startIndex]
                    fDot.dot.move_to((rootRects[i+startIndex].x + rootRects[i+startIndex].w, rootRects[i+startIndex].y, 0))
                    if self.showLabels:
                        fDot.numberLabel.move_to(fDot.dot.get_center())
            elif self.treeLayout == TreeLayout.Centered:
                for i in range(len(self.rootDisplayOrder)-startIndex): 
                    fDot = self.rootDisplayOrder[i+startIndex]
                    widthOfLeftMostChild = 0
                    if len(fDot.children)>0:
                        widthOfLeftMostChild = fDot.children[-1].widthOfChildren
                    fDot.dot.move_to((rootRects[i+startIndex].x + rootRects[i+startIndex].w/2 + widthOfLeftMostChild/4, rootRects[i+startIndex].y, 0))
                    if self.showLabels:
                        fDot.numberLabel.move_to(fDot.dot.get_center())
            elif self.treeLayout == TreeLayout.H_V: #StartIndex doesnt make sense when packing
                for i in range(len(self.rootBinaryTrees)): 
                    self.rootBinaryTrees[i][0].dot.move_to((rootRects[i].x+self.rootDisplayOrder[0].dot.radius*4, rootRects[i].y, 0))

    def sort_root_by_width_height(self):
        if self.treeLayout == TreeLayout.RightAlligned or self.treeLayout == TreeLayout.Centered:
            self.rootDisplayOrder.sort(key=lambda x: (x.heightOfChildren, x.widthOfChildren), reverse=True) 
        if self.treeLayout == TreeLayout.H_V:
            self.rootBinaryTrees.sort(key=lambda x: (x[0].heightOfChildren, x[0].widthOfChildren), reverse=True) 
            newRootOrder = list()
            for x in self.rootBinaryTrees:
                newRootOrder.append(x[0])
            self.rootDisplayOrder = newRootOrder

    def get_index_for_display(self, fDot: FiboNode):
        x = 0
        for i in self.rootDisplayOrder:
            if fDot.id == i.id:
                return x
            x += 1
        return 0
    
    def change_root_packing_and_sorting(self, rootPacking: RootPacking = RootPacking.horizontalPacking, rootSorting: RootSorting = RootSorting.Order, isAnimation: bool = False):
        if rootPacking == self.rootPacking and rootSorting == self.rootSorting:
            return

        if rootPacking != self.rootPacking:
            self.rootPacking = rootPacking
        
        if rootSorting != self.rootSorting:
            self.rootSorting = rootSorting
            if self.rootSorting == RootSorting.Order:
                self.rootDisplayOrder = self.root.copy()
                if self.treeLayout == TreeLayout.H_V:
                    self.restore_order_in_binary_root_list()
        
        if not isAnimation:
            self.sceneUpToDate = False
            return

        self.prepare(isAnimation)
        
        if self.rootSorting == RootSorting.HeightWidth:
            self.sort_root_by_width_height()
            self.animate_trees(self.get_index_for_display(self.rootDisplayOrder[0]))
        else:
            self.animate_trees(0)
        
        self.finish(isAnimation)

    def create_rectangles(self):
        class Rect:
            def __init__(self, height: int, width: int):
                self.x = None
                self.y = None
                self.h = height
                self.w = width

        rootRects = list()
        spacing = self.rootDisplayOrder[0].dot.radius*4

        if self.treeLayout == TreeLayout.RightAlligned:
            for r in self.rootDisplayOrder:
                rootRects.append(Rect(spacing+r.heightOfChildren, spacing+r.widthOfChildren))
            # rootRects[0].x = self.rootDisplayOrder[0].dot.get_x()-(self.rootDisplayOrder[0].widthOfChildren)-spacing #If we want a non moving index 0
            # rootRects[0].y = self.rootDisplayOrder[0].dot.get_y()
            rootRects[0].x = 0#-(self.rootDisplayOrder[0].widthOfChildren)-spacing
            rootRects[0].y = 0
        elif self.treeLayout == TreeLayout.Centered:
            for r in self.rootDisplayOrder:
                rootRects.append(Rect(spacing+r.heightOfChildren, spacing+r.widthOfChildren))
            rootRects[0].x = 0#-(self.rootDisplayOrder[0].widthOfChildren/2)-spacing
            rootRects[0].y = 0
        elif self.treeLayout == TreeLayout.H_V:
            for r in self.rootBinaryTrees:
                rootRects.append(Rect(spacing*2 + r[0].heightOfChildren, spacing*2+r[0].widthOfChildren))
            rootRects[0].x = 0
            rootRects[0].y = 0

        return rootRects
        
    def update_start_index(self, startIndex_ :int):
        if startIndex_ < 0 or startIndex_ >= len(self.rootDisplayOrder) or len(self.root) == 0:
            return

        startIndex = startIndex_
        if self.rootPacking == RootPacking.binaryTreePacking:
            if self.rootSorting == RootSorting.HeightWidth:
                self.sort_root_by_width_height()
            startIndex = 0
            return startIndex
        
        if self.rootSorting == RootSorting.HeightWidth:
            NodeAtChange = self.rootDisplayOrder[startIndex]
            self.sort_root_by_width_height()
            startIndex = self.get_index_for_display(NodeAtChange)

        return startIndex

##############################################################
################### Root Packing functions ###################
    def horizontalPacking(self, boundX_: int, boundY_: int, listOfRects: list):
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

    def nfdh_packing(self, boundX_: int, boundY_: int, listOfRects: list):
        #Only promissed to find a small boundary box if sorted by height. 
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

    def binaryTreePacking(self, boundX: int, boundY: int, listOfRects: list):
        #Breakes the order of roots even if self.rootSorting = RootSorting(Order) 
        #Implementation rewritten from: https://www.david-colson.com/2020/03/10/exploring-rect-packing.html
        class Node():
            def __init__(self, x_: int, y_: int, w_: int, h_: int):
                self.x = x_
                self.y = y_
                self.w = w_
                self.h = h_
        
        freeSpaceNodes = list()
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


##############################################
################### Camera ################### 
    
    def adjust_camera(self, isAnimation):
        self.topMargin = (self.newBounds[1] / self.scalePercentage)-self.newBounds[1] 

        heap_width = self.newBounds[0] 
        new_center = [(heap_width / 2)+0.2, -self.topMargin, 0]

        if isAnimation:
            self.play(self.camera.frame.animate.move_to(new_center).set_width(heap_width+0.4))
        else:
            self.camera.frame.move_to(new_center).set_width(heap_width)

        self.defaultAddPoint[0] = self.camera.frame.get_center()[0]

######################################################
################### Util Functions ###################

    def restore_normal_color(self):
        for x in self.nodeDic.values():
            if isinstance(x, self.FiboNode):
                if x.marked:
                    x.dot.color = ORANGE
                else:
                    x.dot.color = BLUE

        self.min_node.dot.color = RED
    
    def color_by_depth(self):
        self.build_trees(0)
    
    def update_height_of_children(self, parent: FiboNode, child: FiboNode, isAddingNode: bool): 
        if self.treeLayout == TreeLayout.H_V:
            return
        if isAddingNode: 
            newHeight = child.heightOfChildren+self.treeVerticalSpacing
            if parent.heightOfChildren < newHeight:
                parent.heightOfChildren = newHeight
        else:
            if len(parent.children) == 0:
                parent.heightOfChildren = 0
            else:
                hightOfTallestChild = 0
                for c in parent.children:
                    if c.heightOfChildren > hightOfTallestChild:
                        hightOfTallestChild = c.heightOfChildren
                parent.heightOfChildren = hightOfTallestChild + self.treeVerticalSpacing

    def update_width_of_children(self, parent: FiboNode, child: FiboNode, isAddingNode: bool):
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
            while isinstance(Temp_node, self.FiboNode):
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

