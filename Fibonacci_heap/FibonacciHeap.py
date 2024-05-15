import math 
class FibonacciHeap:
    rootList = None
    minFibNode = None
    totalFibNodes = 0
    id = 0
    class FibonacciHeapNode:
        def __init__(self, value, id):
            self.id = id
            self.value = value
            self.parent = self.child = None
            self.left = self.right = self
            self.degree = 0
            self.marked = False

    def insert(self, value):
        newNode = self.FibonacciHeapNode(value, self.id)
        newHeap = FibonacciHeap()
        newHeap.totalFibNodes = 1
        newHeap.minFibNode = newHeap.rootList = newNode
        update = self.meld_heaps(newHeap)
        self.id += 1
        return (newNode, update)

    #updates min if node is smaller than current min
    def update_min_with_single_node(self, fibNode):
        if self.minFibNode is None or fibNode.value <= self.minFibNode.value:
            self.minFibNode = fibNode
            return True
        else: 
            return False
   
    #iterates the circular doubly linked list and updates min node
    def set_new_min_from_root_list(self):
        currentNode = self.rootList.right
        while True: 
            self.update_min_with_single_node(currentNode)
            if self.rootList == currentNode:
                break
            currentNode = currentNode.right

    #return min node in O(1) time
    def return_min(self):
        return self.minFibNode

    #Merge two heaps by appending nodes to root list of first heap
    def meld_heaps(self, heap_two):
        if self.rootList is None and heap_two.rootList is not None:
            self.rootList = heap_two.rootList
            self.minFibNode = heap_two.minFibNode
            self.totalFibNodes = heap_two.totalFibNodes
            return True
        elif self.rootList is not None and heap_two.rootList is not None:
            new_end = heap_two.rootList.left
            self.rootList.left.right = heap_two.rootList
            heap_two.rootList.left.right = self.rootList
            heap_two.rootList.left = self.rootList.left
            self.rootList.left = new_end
            self.totalFibNodes += heap_two.totalFibNodes 
            return self.update_min_with_single_node(heap_two.minFibNode)

    # insert a node in the circular doubly linked list rootList - will be inserted as new root  
    def meld_node_into_root_list(self, node_to_insert):
        if self.rootList is not None:
            node_to_insert.left = self.rootList.left 
            node_to_insert.right = self.rootList
            self.rootList.left.right = node_to_insert
            self.rootList.left = node_to_insert 
        else:
            self.rootList = node_to_insert
    
    #Removes node from root list 
    def remove_node_from_root_list(self, fibNode):
        if fibNode == fibNode.left:
            self.minFibNode = None
            self.rootList = None
        else:
            fibNode.left.right = fibNode.right
            fibNode.right.left = fibNode.left
            self.rootList = fibNode.right if fibNode == self.rootList else self.rootList
        #reset linked nodes to itself 
        fibNode.right = fibNode
        fibNode.left = fibNode

    # insert a node in the circular doubly linked child list of a parent - will be inserted as new root  
    def meld_node_into_child_list(self, fibNodeChild, fibNodeParent):
        if fibNodeParent.child is not None:
            fibNodeChild.left = fibNodeParent.child.left 
            fibNodeChild.right = fibNodeParent.child 
            fibNodeParent.child.left.right = fibNodeChild 
            fibNodeParent.child.left = fibNodeChild
        else:
            fibNodeParent.child = fibNodeChild 
    
    #Removes node from child list 
    def remove_node_from_child_list(self, fibNode):
        if fibNode == fibNode.left:
            fibNode.parent.child = None
        else:
            fibNode.left.right = fibNode.right
            fibNode.right.left = fibNode.left
            if fibNode == fibNode.parent.child:
                fibNode.parent.child = fibNode.right
        fibNode.parent.degree -= 1
        #reset linked nodes to itself and update parent
        fibNode.right = fibNode
        fibNode.left = fibNode
        fibNode.parent = None

    #Extract min and update heap
    def extract_min(self):
        if self.rootList is not None:
            minNode = self.minFibNode
            #Add all children to to root list if any
            if minNode.child is not None:
                current_child = minNode.child
                while True:
                    next_child = current_child.right
                    self.cut(current_child)
                    if minNode.child is None:
                        break
                    current_child = next_child

            #set new min to next 
            self.minFibNode = minNode.right

            #remove min node from root
            self.remove_node_from_root_list(minNode)
            self.totalFibNodes -= 1
            actions = []
            #Consolidate and set new min unless rootList is only one root or empty - the only child of the removed min
            if self.rootList is not None:
                if self.rootList != self.rootList.right:
                    actions = self.consolidate()
                self.set_new_min_from_root_list()
            return (minNode, actions, self.minFibNode)

    #Map heap until no root has same degree
    def consolidate(self):
        actions = []
        max_degree = int(math.log(self.totalFibNodes, (1 + math.sqrt(5)) / 2)) 
        array = [None] * (max_degree + 1)
        array[self.rootList.degree] = self.rootList
        end_node = self.rootList.left
        currentNode = self.rootList.right

        while True: 
            next_node = currentNode.right
            if array[currentNode.degree] is None:
                array[currentNode.degree] = currentNode
            else:
                nodes = self.link_nodes(array[currentNode.degree], currentNode)
                node = nodes[0]
                actions.append((nodes[0], nodes[1]))
                array[node.degree-1] = None
                while node.degree <= max_degree-1 and array[node.degree] is not None:
                    nodes = self.link_nodes(array[node.degree], node)
                    node = nodes[0]
                    actions.append((nodes[0], nodes[1]))
                    array[node.degree-1] = None
                array[node.degree] = node
            if currentNode == end_node:
                break
            currentNode = next_node

        return actions

    #Link two nodes together - one will become child, other parent 
    def link_nodes(self, fibNodeOne, fibNodeTwo):
            fibNodeChild = fibNodeOne if fibNodeOne.value >= fibNodeTwo.value else fibNodeTwo
            if fibNodeChild.marked: 
                fibNodeChild.marked = False
            fibNodeParent = fibNodeOne if fibNodeTwo.value > fibNodeOne.value else fibNodeTwo
            self.remove_node_from_root_list(fibNodeChild)
            self.meld_node_into_child_list(fibNodeChild, fibNodeParent)
            fibNodeChild.parent = fibNodeParent
            fibNodeParent.degree += 1
            return (fibNodeParent, fibNodeChild)

    #function to decrease value of a node - eg. 46 -> 12 FIX IF HEAP PROP NOT VIOLATED
    def decrease_value(self, nodetoDecrease, newValue):
        if nodetoDecrease.value > newValue:
            nodetoDecrease.value = newValue
            parent = nodetoDecrease.parent
            actions = []
            if parent is not None and parent.value > newValue:
                cutNodeInfo = self.cut(nodetoDecrease)
                actions.append(cutNodeInfo)
                actions = self.cascading_cut(parent, actions)

            update = self.update_min_with_single_node(nodetoDecrease) 
            return (nodetoDecrease, actions, update)

    #Cut node from child list to root 
    def cut(self, nodeToCut):
        self.remove_node_from_child_list(nodeToCut)
        self.meld_node_into_root_list(nodeToCut)
        mark = nodeToCut.marked
        if nodeToCut.marked:
            nodeToCut.marked = False
        return (nodeToCut, mark)
        
    # handle parent of cut node in decreasing a value
    def cascading_cut(self, decreasedNodeParent, actions):
        if decreasedNodeParent.parent is not None:
            if not decreasedNodeParent.marked:
                decreasedNodeParent.marked = True
                actions.append(decreasedNodeParent)
                return actions
            else:
                next_parent = decreasedNodeParent.parent
                cutNodeInfo = self.cut(decreasedNodeParent)
                actions.append(cutNodeInfo)
                self.cascading_cut(next_parent, actions)
                return actions
        else:
            return actions
    
    def delete(self, node):
        self.decrease_value(node, -float('inf'))
        self.extract_min()

    #Helper functions to print heap to console
    def print_heap(self):
        if self.rootList is not None:
            print()
            print("-----------------------------------------------------")
            print("|              Fibonacci Heap Structure             |")
            print("-----------------------------------------------------")
            print()
            firstNode = self.rootList
            currentNode = self.rootList.right
            flag = True
            while flag:
                if currentNode == firstNode:
                    flag = False
                print("|")
                if currentNode.marked:
                    print("---", currentNode.value, "+")
                else:
                    print("---", currentNode.value)
                if currentNode.child is not None:
                    self.recursive_print(currentNode, 1)
                currentNode = currentNode.right
                print()

    def recursive_print(self, node, degree):
        firstNode = node.child
        currentNode = node.child.right
        flag = True
        s = "  "

        while flag:
            if currentNode == firstNode:
                flag = False
            print(s*degree, "|")
            if currentNode.marked:
                print(s*degree, "---", currentNode.value, "+")
            else: 
                print(s*degree, "---", currentNode.value)
            if currentNode.child is not None:
                self.recursive_print(currentNode, degree+2)
            currentNode = currentNode.right