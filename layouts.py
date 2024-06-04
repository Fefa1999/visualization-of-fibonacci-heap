import FiboScene
from manim import *
from manim.typing import Point3D
from manim.typing import Vector3
import math

ColorPalet = list(map(ManimColor, [(146,43,33), (231,76,60), (142,68,173), (155,89,182), (41,128,185), 
                (52,152,219), (20,90,50), (30,132,73), (39,174,96), (88,214,141),
                (211,84,0), (230,126,34), (243,156,18), (241,196,15)]))

def get_color_from_depth(depth: int):
    if depth < 0:
        return

    return ColorPalet[depth%14]

########################################################
################### Layout Interface ###################
class Layout_Interface:
    def __init__(self) -> None:
        pass
    
    def build_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int) -> None:
        #Build the trees from the starting index, to end, returns nothing
        pass

    def animate_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int) -> list[FiboScene.FiboScene.FiboNode]:
        #Set the targets of all FiboNodes in affected trees. Return a list of Nodes that have changed position.
        pass

    def spaceRootTrees(self, rootList: list[FiboScene.FiboScene.FiboNode], isAnimation: bool) -> None:
        pass


##########################################################################
################### Allign with parent right - Layout. ###################
class Rigth_Allinged_Layout(Layout_Interface):
    def __init__(self, verticalSpacing : int = 1.5) -> None:
        self.treeVerticalSpacing = verticalSpacing
        super().__init__()
  
    def animate_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex:int):
        for i in range(len(rootList)-startIndex):
            x = rootList[i+startIndex]
            self.create_children_animations(x, x.dot.target)

    def create_children_animations(self, parentMojb: FiboScene.FiboScene.FiboNode, parentTarget: Dot):
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
            self.create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target)
        return
    
    def build_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int):
        for i in range(len(rootList)-startIndex):
            self.move_children(self.rootDisplayOrder[i+startIndex])

    def move_children(self, parentMojb: FiboScene.FiboScene.FiboNode):
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
            self.move_children(n)
    
    def recalculate_tree_dimensions(self, rootDot: FiboScene.FiboScene.FiboNode):

        distance = self.root[0].dot.radius*4

        def updated(fDot: self.FiboNode):
            if not isinstance(fDot, self.FiboNode):
                return #Error
            
            if len(fDot.children) == 0:
                fDot.widthOfChildren = 0 
                fDot.heightOfChildren = 0
                return (0, 0)

            if len(fDot.children) == 1:
                fDot.widthOfChildren = 0
                fDot.heightOfChildren = self.treeVerticalSpacing
                return (0, self.treeVerticalSpacing)
            
            width = 0
            height = 0
            for i in fDot.children:
                updated(i)
                width += i.widthOfChildren
                height = max(height, i.heightOfChildren)
            fDot.widthOfChildren = width+distance*(len(fDot.children)-1)
            fDot.heightOfChildren = height+self.treeVerticalSpacing
                
            return fDot.heightOfChildren, fDot.widthOfChildren

        updated(rootDot)

    def space_children_by_thier_own_width(self, lst: list[FiboScene.FiboScene.FiboNode], isToTarget: bool = False, direction: Vector3 = LEFT, **kwargs):
        if isToTarget:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.target.next_to(m1.dot.target, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        else:
            for m1, m2 in zip(lst, lst[1:]):
                m2.dot.next_to(m1.dot, direction, (m1.widthOfChildren + m1.dot.radius*2), **kwargs)
        return lst
    

######################################################
################### Centered Trees ###################   
class Centered_Layout(Layout_Interface):
    def __init__(self) -> None:
        super().__init__()

    def animate_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex):
        for i in range(len(rootList)-startIndex):
            x = rootList[i+startIndex]
            self.cen_create_children_animations(x, x.dot.target)

    def cen_create_children_animations(self, parentMojb: FiboScene.FiboScene.FiboNode, parentTarget: Dot):
        if len(parentMojb.children)==0:
            return

        #First child which the other children should be alinged left of
        baseChild = parentMojb.children[0]
        baseChild.dot.target = Dot(point=baseChild.dot.get_center(), radius=baseChild.dot.radius, color=baseChild.dot.color).set_y(parentTarget.get_y()-self.treeVerticalSpacing).set_x(parentTarget.get_x()+parentMojb.widthOfChildren/2-parentMojb.children[-1].widthOfChildren/4-parentMojb.children[0].widthOfChildren/2)
        self.mobjsToMove.append(baseChild)

        for i in range(len(parentMojb.children)-1):
            child =  parentMojb.children[i+1]
            child.dot.target = Dot(point=child.dot.get_center(), radius=child.dot.radius, color=child.dot.color)
            self.mobjsToMove.append(child)
        
        #Arrange based on first child.
        self.space_children_by_half_their_width(parentMojb.children, True)

        for n in range(len(parentMojb.children)):
            self.cen_create_children_animations(parentMojb.children[n], parentMojb.children[n].dot.target)
        return

    def build_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int):
        for i in range(len(rootList)-startIndex):
            self.move_children(rootList[i+startIndex])

    def move_children(self, parentMojb: FiboScene.FiboScene.FiboNode):
        if len(parentMojb.children)==0:
            return
        
        #Set first childs new location
        baseChild = parentMojb.children[0]
        baseChild.dot.set_y(parentMojb.dot.get_y()-self.treeVerticalSpacing).set_x(parentMojb.dot.get_x()+parentMojb.widthOfChildren/2-parentMojb.children[-1].widthOfChildren/4-parentMojb.children[0].widthOfChildren/2)
        
        #Arrange rest based on first
        self.space_children_by_half_their_width(parentMojb.children, False)

        #Move arrows and recursively move childrens og children
        parentsCenter = parentMojb.dot.get_center()
        for n in parentMojb.children:
            if self.showLabels:
                n.numberLabel.move_to(n.dot.get_center())
            n.arrow.put_start_and_end_on(n.dot.get_center(), parentsCenter)
            self.move_children(n)

    def space_children_by_half_their_width(self, lst: list[FiboScene.FiboScene.FiboNode], isToTarget: bool = False, **kwargs):
        for m1, m2 in zip(lst, lst[1:]): 
            m1_left_width = m1.widthOfChildren/2
            m2_rigth_width = m2.widthOfChildren/2
            if len(m1.children)>0:
                m1_left_width = m1.widthOfChildren/2+m1.children[-1].widthOfChildren/4
            if len(m2.children)>0:
                m2_rigth_width = m2.widthOfChildren/2-m2.children[-1].widthOfChildren/4

            if isToTarget:
                m2.dot.target.next_to(m1.dot.target, LEFT, (m1_left_width + m2_rigth_width + m1.dot.radius*2), **kwargs)
            else:
                m2.dot.next_to(m1.dot, LEFT, (m1_left_width + m2_rigth_width + m1.dot.radius*2), **kwargs)
        return lst


###############################################
################### HV-Tree ###################
class HV_Tree_Layout(Layout_Interface):
    def __init__(self) -> None:
        self.rootBinaryTrees = list()
        super().__init__()

    def animate_Tree(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int):
        if startIndex < 0 or startIndex >= len(rootList):
            return

        def aux(i: int, isLeftIsClosest: bool, x: float, y: float, depth_: int):
            currentDot = ba[i]
            if not isinstance(currentDot, self.FiboNode):
                return
            
            depth = depth_

            color_ = currentDot.dot.color
            if self.showDepthColor:
                color_ = self.get_color_from_depth(depth)
            currentDot.dot.target = Dot(point=(currentDot.dot.get_center()), radius=currentDot.dot.radius, color=color_)
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
                rigthV = rigth.heightOfChildren
    

            leftY= 0.0; rightX = 0.0
            dt = currentDot.dot.target

            if currentDot.id != -1:
                isLeftIsClosest = (len(currentDot.children)%2==0)


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

        for i in range((len(rootList))-startIndex):
            fDot = rootList[i+startIndex]
            if len(fDot.children) == 0:
                continue
            standardDistance = fDot.dot.radius*4
            ba = self.rootBinaryTrees[i+startIndex]
            if ba[2] == None and ba[1] == None: # if the tree have changed.
                self.rootBinaryTrees[i+startIndex] = self.transform_to_binary(fDot) 
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

    def hv_Tree_Build(self, rootList: list[FiboScene.FiboScene.FiboNode], startIndex: int):
        if startIndex < 0 or startIndex >= len(rootList):
            return

        def aux(realParent: FiboScene.FiboScene.FiboNode, i: int, isLeftIsClosest: bool, x: float, y: float, depth_: int):
            currentDot = ba[i]
            if not isinstance(currentDot, FiboScene.FiboScene.FiboNode):
                return
            
            depth = depth_

            currentDot.dot.move_to((x,y,0))
            if self.showLabels and currentDot.id != -1:
                currentDot.numberLabel.move_to(currentDot.dot.get_center())
            if currentDot.arrow is not None:
                currentDot.arrow.put_start_and_end_on(currentDot.dot.get_center(), self.nodeDic[currentDot.parentKey].dot.get_center())
            if self.showDepthColor:
                currentDot.dot.color = get_color_from_depth(depth)

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
                rigthV = rigth.heightOfChildren

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


        for i in range((len(rootList)-startIndex)):
            fDot = rootList[i+startIndex]
            standardDistance = fDot.dot.radius*4
            ba = self.rootBinaryTrees[i+startIndex]
            if len(fDot.children) > 0 and ba[2] == None and ba[1] == None:
                ba = self.transform_to_binary(fDot) 
            maxIndex = len(ba)
            isLeftIsClosest_ = (len(fDot.children)%2==0)
            aux(0, isLeftIsClosest_, fDot.dot.get_x(), fDot.dot.get_y(), 0)
        
        return 

    def transform_to_binary(self, parrentDot: FiboScene.FiboScene.FiboNode):
        binaryArray = [None] * (max(1,int(math.ceil(parrentDot.nFdotsInTree*1.25*2))))

        def aux(binaryIndex, fDot: FiboScene.FiboScene.FiboNode):
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

                fakeDot = FiboScene.FiboScene.FiboNode(-1)
                fakeDot.dot = Dot()
                binaryArray[currentIndex] = fakeDot

                aux(currentIndex*2+2-childN%2, fDot.children[childN-1])
                childN -= 1
                currentIndex = currentIndex*2+2-childN%2

        aux(0,parrentDot)
        self.recalculate_binary_tree_dimensions(binaryArray, len(parrentDot.children)%2==0)
        return binaryArray
    
    def recalculate_binary_tree_dimensions(self, binaryHeap: list[FiboScene.FiboScene.FiboNode], leftIsClosest: bool):  
        root = binaryHeap[0]
        distance = root.dot.radius*4
        maxIndex = len(binaryHeap)

        def updated(i: int, leftIsClosest_: bool):
            fDot = binaryHeap[i]
            if not isinstance(fDot, self.FiboNode):
                return 0,0

            fDot.widthOfChildren = 0
            fDot.heightOfChildren = 0

            if i*2+2 >= maxIndex:
                return 0, 0
            
            leftHeight = 0; leftWidth = 0
            if fDot.id != -1:
                leftIsClosest_ = (len(fDot.children)%2==0)
            if binaryHeap[i*2+1] is not None:
                leftHeight, leftWidth = updated(i*2+1, (not leftIsClosest_))
                leftHeight += distance

            rigthHeight = 0; rigthWidth = 0
            if binaryHeap[i*2+2] is not None:
                rigthHeight, rigthWidth = updated(i*2+2, (not leftIsClosest_))
                rigthWidth += distance

            if leftIsClosest_:
                fDot.widthOfChildren = rigthWidth+leftWidth
                fDot.heightOfChildren = max(rigthHeight, leftHeight)
            else:
                fDot.widthOfChildren = max(leftWidth, rigthWidth)
                fDot.heightOfChildren = rigthHeight+leftHeight
                
            return fDot.heightOfChildren, fDot.widthOfChildren

        updated(0, leftIsClosest)

    def restore_order_in_binary_root_list(self, rootList: list[FiboScene.FiboScene.FiboNode]):
        newBinRoot = list ()
        for i in rootList:
            for x in self.rootBinaryTrees:
                if x[0].id == i.id:
                    newBinRoot.append(x)
                    break
        self.rootBinaryTrees = newBinRoot






























