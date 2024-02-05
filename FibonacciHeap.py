import math 
import array as arr

class FibonacciHeap:
    root_list = None
    min_fibNode = None
    total_fibNodes = 0

    class FibonacciHeapNode:
        def __init__(self, key):
            self.key = key
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.marked = False
    
    #create and insert a node in the root list in O(1) time
    def insert(self, key):
        new_node = self.FibonacciHeapNode(key)
        new_node.left = new_node.right = new_node
        self.insert_node_in_root_list(new_node)
        self.check_min_with_single_node(new_node)
        self.total_fibNodes += 1

    #updates min if node is smaller than current min
    def check_min_with_single_node(self, fibNode):
        if self.min_fibNode is None or fibNode.key < self.min_fibNode.key:
            self.min_fibNode = fibNode
   
    #iterates the circular doubly linked list and updates min node
    def set_new_min_from_root_list(self):
        head = self.root_list
        currentNode = head.right
        self.check_min_with_single_node(head)
        while head != currentNode:
            self.check_min_with_single_node(currentNode)
            currentNode = currentNode.right

    #return min node in O(1) time
    def returnMin(self):
        return self.min_fibNode

    # insert a node in the circular doubly linked list root_list - will be inserted as new root  
    def insert_node_in_root_list(self, nodeToInsert):
        if self.root_list is None:
            self.root_list = nodeToInsert
        else:
            nodeToInsert.left = self.root_list.left 
            nodeToInsert.right = self.root_list  
            self.root_list.left.right = nodeToInsert 
            self.root_list.left = nodeToInsert 
            self.root_list = nodeToInsert 
        

    #Removes node from root list 
    def remove_node_from_root_list(self, fibNode):
        if fibNode == fibNode.left:
                self.min_fibNode = None
                self.root_list = None
        else:
            fibNode.left.right = fibNode.right
            fibNode.right.left = fibNode.left
            self.root_list = fibNode.right if fibNode == self.root_list else self.root_list
        fibNode.right = fibNode
        fibNode.left = fibNode
    
     #Removes node from root list 
    def remove_node_from_child_list(self, fibNode):
        if fibNode == fibNode.left:
                fibNode.parent.child = None
        else:
            fibNode.left.right = fibNode.right
            fibNode.right.left = fibNode.left
            fibNode.parent.child = fibNode.right if fibNode == fibNode.parent.child else fibNode.parent.child
        fibNode.right = fibNode
        fibNode.left = fibNode
        fibNode.parent = None

    def extract_min(self):
        min_node = self.min_fibNode
        #Add all children to to root list if any
        if min_node.child is not None:
            currentChild = min_node.child.right
            flag = True
            #move children of min to root list
            while flag:
                if min_node.child == currentChild:
                    flag = False
                tempChild = currentChild.right
                self.remove_node_from_child_list(currentChild)
                self.insert_node_in_root_list(currentChild)
                currentChild = tempChild

        #set new min to next 
        self.min_fibNode = min_node.right 

        #remove min node from root
        self.remove_node_from_root_list(min_node)
        self.total_fibNodes -= 1

        #Consolidate and set new min unless root_list is only one root 
        if self.root_list != self.root_list.right:
            self.consolidate()
            self.set_new_min_from_root_list()

        return min_node

    def consolidate(self):
        maxDegree = int(math.log(self.total_fibNodes, (1 + math.sqrt(5)) / 2)) + 1
        array = [None] * (maxDegree + 1)
        array[self.root_list.degree] = self.root_list
        endNode = self.root_list.left
        currentNode = self.root_list.right

        while True: 
            tempNode = currentNode.right
            if array[currentNode.degree] is None:
                array[currentNode.degree] = currentNode
            else:
                node = self.union(array[currentNode.degree], currentNode) if array[currentNode.degree].key > currentNode.key else self.union(currentNode, array[currentNode.degree])
                array[node.degree-1] = None
                while node.degree <= maxDegree-1 and array[node.degree] is not None:
                    array[node.degree-1] = None
                    node = self.union(array[node.degree], node) if array[node.degree].key > node.key else self.union(node, array[node.degree])
                array[node.degree-1] = None
                array[node.degree] = node
            if currentNode == endNode:
                break
            currentNode = tempNode

    def union(self, fibNodeChild, fibNodeParent):
            self.remove_node_from_root_list(fibNodeChild)
            self.insert_node_in_child_list(fibNodeChild, fibNodeParent)
            fibNodeChild.parent = fibNodeParent
            fibNodeParent.degree += 1
            return fibNodeParent
    
    def insert_node_in_child_list(self, fibNodeChild, fibNodeParent):
        if fibNodeParent.child is None:
            fibNodeParent.child = fibNodeChild
        else:
            fibNodeChild.left = fibNodeParent.child.left 
            fibNodeChild.right = fibNodeParent.child 
            fibNodeParent.child.left.right = fibNodeChild 
            fibNodeParent.child.left = fibNodeChild 
            fibNodeParent.child = fibNodeChild 

    
    def printHeap(self):
        print()
        print("-----------------------------------------------------")
        print("|              Fibonacci Heap Structure             |")
        print("-----------------------------------------------------")
        print()

        firstNode = self.root_list
        currentNode = self.root_list.right
        flag = True

        while flag:
            if currentNode == firstNode:
                flag = False
            print("|")
            print("---", currentNode.key)
            if currentNode.child is not None:
                self.recursivePrint(currentNode, 1)
            currentNode = currentNode.right
            print()
    def recursivePrint(self, node, degree):
        firstNode = node.child
        currentNode = node.child.right
        flag = True
        s = "  "

        while flag:
            if currentNode == firstNode:
                flag = False
            print(s*degree, "|")
            print(s*degree, "---", currentNode.key)
            if currentNode.child is not None:
                self.recursivePrint(currentNode, degree+2)
            currentNode = currentNode.right

# Function to create and run the Fibonacci heap
def run():
    heap = FibonacciHeap()

    for i in range(300, -1, -1):
        heap.insert(i)
    #for i in range(21):
        #heap.insert(i)
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
    heap.extract_min().key
    heap.printHeap()
# Run the function
run()
