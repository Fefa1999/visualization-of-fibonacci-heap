import math 
import array as arr
class FibonacciHeap:
    root_list = None
    min_fib_node = None
    total_fib_nodes = 0

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
        self.total_fib_nodes += 1

    #updates min if node is smaller than current min
    def check_min_with_single_node(self, fib_node):
        if self.min_fib_node is None or fib_node.key < self.min_fib_node.key:
            self.min_fib_node = fib_node
   
    #iterates the circular doubly linked list and updates min node
    def set_new_min_from_root_list(self):
        current_node = self.root_list.right
        while True: 
            self.check_min_with_single_node(current_node)
            if self.root_list == current_node:
                break
            current_node = current_node.right

    #return min node in O(1) time
    def returnMin(self):
        return self.min_fib_node

    # insert a node in the circular doubly linked list root_list - will be inserted as new root  
    def insert_node_in_root_list(self, node_to_insert):
        if self.root_list is not None:
            node_to_insert.left = self.root_list.left 
            node_to_insert.right = self.root_list  
            self.root_list.left.right = node_to_insert 
            self.root_list.left = node_to_insert 
        self.root_list = node_to_insert 

    #Removes node from root list 
    def remove_node_from_root_list(self, fib_node):
        if fib_node == fib_node.left:
            self.min_fib_node = None
            self.root_list = None
        else:
            fib_node.left.right = fib_node.right
            fib_node.right.left = fib_node.left
            self.root_list = fib_node.right if fib_node == self.root_list else self.root_list
        #reset linked nodes to itself 
        fib_node.right = fib_node
        fib_node.left = fib_node

    # insert a node in the circular doubly linked child list of a parent - will be inserted as new root  
    def insert_node_in_child_list(self, fib_node_child, fib_node_parent):
        if fib_node_parent.child is not None:
            fib_node_child.left = fib_node_parent.child.left 
            fib_node_child.right = fib_node_parent.child 
            fib_node_parent.child.left.right = fib_node_child 
            fib_node_parent.child.left = fib_node_child 
        fib_node_parent.child = fib_node_child 
    
     #Removes node from root list 
    def remove_node_from_child_list(self, fib_node):
        if fib_node == fib_node.left:
            fib_node.parent.child = None
        else:
            fib_node.left.right = fib_node.right
            fib_node.right.left = fib_node.left
            if fib_node == fib_node.parent.child:
                fib_node.parent.child = fib_node.right
        #reset linked nodes to itself and update parent
        fib_node.right = fib_node
        fib_node.left = fib_node
        fib_node.parent = None

    def extract_min(self):
        min_node = self.min_fib_node
        #Add all children to to root list if any
        if min_node.child is not None:
            current_child = min_node.child.right
            while True:
                next_child = current_child.right
                self.remove_node_from_child_list(current_child)
                self.insert_node_in_root_list(current_child)
                if min_node.child is None:
                    break
                current_child = next_child

        #set new min to next 
        self.min_fib_node = min_node.right 

        #remove min node from root
        self.remove_node_from_root_list(min_node)
        self.total_fib_nodes -= 1

        #Consolidate and set new min unless root_list is only one root - the only child of the removed min
        if self.root_list != self.root_list.right:
            self.consolidate()
            self.set_new_min_from_root_list()

        return min_node

    def consolidate(self):
        max_degree = int(math.log(self.total_fib_nodes, (1 + math.sqrt(5)) / 2)) + 1
        array = [None] * (max_degree + 1)
        array[self.root_list.degree] = self.root_list
        end_node = self.root_list.left
        current_node = self.root_list.right

        while True: 
            next_node = current_node.right
            if array[current_node.degree] is None:
                array[current_node.degree] = current_node
            else:
                node = self.union(array[current_node.degree], current_node)
                array[node.degree-1] = None
                while node.degree <= max_degree-1 and array[node.degree] is not None:
                    node = self.union(array[node.degree], node)
                    array[node.degree-1] = None
                array[node.degree] = node
            if current_node == end_node:
                break
            current_node = next_node

    def union(self, fib_node_one, fib_node_two):
            fib_node_child = fib_node_one if fib_node_one.key > fib_node_two.key else fib_node_two
            fib_node_parent = fib_node_one if fib_node_two.key > fib_node_one.key else fib_node_two
            self.remove_node_from_root_list(fib_node_child)
            self.insert_node_in_child_list(fib_node_child, fib_node_parent)
            fib_node_child.parent = fib_node_parent
            fib_node_parent.degree += 1
            return fib_node_parent
    
    def printHeap(self):
        print()
        print("-----------------------------------------------------")
        print("|              Fibonacci Heap Structure             |")
        print("-----------------------------------------------------")
        print()

        firstNode = self.root_list
        current_node = self.root_list.right
        flag = True

        while flag:
            if current_node == firstNode:
                flag = False
            print("|")
            print("---", current_node.key)
            if current_node.child is not None:
                self.recursivePrint(current_node, 1)
            current_node = current_node.right
            print()
    def recursivePrint(self, node, degree):
        firstNode = node.child
        current_node = node.child.right
        flag = True
        s = "  "

        while flag:
            if current_node == firstNode:
                flag = False
            print(s*degree, "|")
            print(s*degree, "---", current_node.key)
            if current_node.child is not None:
                self.recursivePrint(current_node, degree+2)
            current_node = current_node.right

# Function to create and run the Fibonacci heap
def run():
    heap = FibonacciHeap()

    for i in range(20, -1, -1):
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
