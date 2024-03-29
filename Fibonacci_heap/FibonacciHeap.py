import math 
class FibonacciHeap:
    root_list = None
    min_fib_node = None
    total_fib_nodes = 0
    id = 0
    isAnimation = None
    showExplanatoryText = None
    scene = None
    class FibonacciHeapNode:
        def __init__(self, value):
            self.id = None
            self.value = value
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.marked = False
    
    #create and insert a node in the root list in O(1) time
    def insert(self, value):
        new_node = self.FibonacciHeapNode(value)
        new_node.left = new_node.right = new_node
        new_node.id = self.id
        self.id += 1
        self.merge_node_with_root_list(new_node)
        if self.scene is not None:
            self.scene.insert_dot(new_node.value, self.isAnimation, new_node.id)
        self.check_min_with_single_node(new_node, True)
        self.total_fib_nodes += 1
        return new_node

    #updates min if node is smaller than current min
    def check_min_with_single_node(self, fib_node, print):
        if self.min_fib_node is None or fib_node.value <= self.min_fib_node.value:
            self.min_fib_node = fib_node
            if print:
                self.scene.set_min(fib_node.id, self.isAnimation)
   
    #iterates the circular doubly linked list and updates min node
    def set_new_min_from_root_list(self):
        current_node = self.root_list.right
        while True: 
            self.check_min_with_single_node(current_node, False)
            if self.root_list == current_node:
                break
            current_node = current_node.right
        self.scene.set_min(self.min_fib_node.id, self.isAnimation)

    #return min node in O(1) time
    def returnMin(self):
        return self.min_fib_node

    #Merge two heaps by appending nodes to root list of first heap
    def merge_heaps(self, heap_two):
        end_node = heap_two.root_list
        start_node = heap_two.root_list.right
        while True:
            next_node = start_node.right
            heap_two.remove_node_from_root_list(start_node)
            heap_two.total_fib_nodes -= 1
            self.merge_node_with_root_list(start_node)
            self.check_min_with_single_node(start_node)
            self.total_fib_nodes += 1
            if end_node == start_node:
                break
            start_node = next_node

    # insert a node in the circular doubly linked list root_list - will be inserted as new root  
    def merge_node_with_root_list(self, node_to_insert):
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
    def merge_node_with_child_list(self, fib_node_child, fib_node_parent):
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
        fib_node.parent.degree -= 1
        #reset linked nodes to itself and update parent
        fib_node.right = fib_node
        fib_node.left = fib_node
        fib_node.parent = None

    #Extract min and update heap
    def extract_min(self):
        if self.root_list is not None:
            min_node = self.min_fib_node
            #Add all children to to root list if any
            if min_node.child is not None:
                current_child = min_node.child.right
                while True:
                    next_child = current_child.right
                    self.remove_node_from_child_list(current_child)
                    self.merge_node_with_root_list(current_child)
                    if min_node.child is None:
                        break
                    current_child = next_child

            #set new min to next 
            self.min_fib_node = min_node.right

            #remove min node from root
            self.remove_node_from_root_list(min_node)
            self.scene.delete(min_node.id, self.isAnimation)
            self.total_fib_nodes -= 1

            #Consolidate and set new min unless root_list is only one root or empty - the only child of the removed min
            if self.root_list is not None:
                if self.root_list != self.root_list.right:
                    self.consolidate()
                self.set_new_min_from_root_list()
            return min_node

    #Map heap until no root has same degree
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
                node = self.link_nodes(array[current_node.degree], current_node)
                array[node.degree-1] = None
                while node.degree <= max_degree-1 and array[node.degree] is not None:
                    node = self.link_nodes(array[node.degree], node)
                    array[node.degree-1] = None
                array[node.degree] = node
            if current_node == end_node:
                break
            current_node = next_node

        #self.scene.adjust_camera_after_consolidate(self.isAnimation) #TODO should it be used?

    #Link to nodes toegether - one will become child, other parent 
    def link_nodes(self, fib_node_one, fib_node_two):
            fib_node_child = fib_node_one if fib_node_one.value >= fib_node_two.value else fib_node_two
            fib_node_parent = fib_node_one if fib_node_two.value > fib_node_one.value else fib_node_two
            self.remove_node_from_root_list(fib_node_child)
            self.merge_node_with_child_list(fib_node_child, fib_node_parent)
            fib_node_child.parent = fib_node_parent
            fib_node_parent.degree += 1
            if self.scene is not None:
                self.scene.create_child(fib_node_parent.id, fib_node_child.id, self.isAnimation, self.showExplanatoryText)
            return fib_node_parent

    #function to decrease value of a node - eg. 46 -> 12 
    def decrease_value(self, node_to_decrease_id, new_value):
        node_to_decrease = self.find_node_by_id(self.root_list, node_to_decrease_id)
        if node_to_decrease.value > new_value:
            node_to_decrease.value = new_value
            parent = node_to_decrease.parent
            self.scene.change_key(node_to_decrease.id, new_value, self.isAnimation, self.showExplanatoryText)
            if parent is not None and parent.value > new_value:
                self.cut(node_to_decrease)
                self.cascading_cut(parent)

            self.check_min_with_single_node(node_to_decrease, True) #TODO fix 2ønd parameter

    def find_node_by_id(self, start_node, id):
        current_node = start_node
        while True:
            if current_node.id == id:
                return current_node

            if current_node.child is not None:
                found_node = self.find_node_by_id(current_node.child, id)
                if found_node is not None:  
                    return found_node

            if current_node.right == start_node:
                break  
            else:
                current_node = current_node.right
        return None

    #Cut node from child list to root 
    def cut(self, node_to_cut):
        self.remove_node_from_child_list(node_to_cut)
        self.merge_node_with_root_list(node_to_cut)
        self.scene.cut(node_to_cut.id, self.isAnimation, node_to_cut.marked, self.showExplanatoryText)
        if node_to_cut.marked:
            node_to_cut.marked = False
    
    # handle parent of cut node in decreasing a value
    def cascading_cut(self, decreased_node_parent):
        if decreased_node_parent.parent is not None:
            if not decreased_node_parent.marked:
                decreased_node_parent.marked = True
                self.scene.cascading_cut(decreased_node_parent.id, self.isAnimation, self.showExplanatoryText)
            else:
                next_parent = decreased_node_parent.parent
                self.cut(decreased_node_parent)
                self.cascading_cut(next_parent)

    def delete_node(self, node_to_delete):
        self.decrease_value(node_to_delete, -float('inf'))
        self.extract_min()
    
    def increaseKey(self, node_to_increase, value):
        self.decrease_value(node_to_increase, -float('inf'))
        self.extract_min()
        self.insert(value)

    def find_deepest_node(self):
        current_node = self.root_list.right
        end_node = self.root_list
        deepest_root_node = current_node
        while True:
            if current_node == end_node:
                break 
            if deepest_root_node.degree < current_node:
                deepest_root_node = current_node
            current_node = current_node.right

        while True:
            if deepest_root_node.child is None:
                break
            else:
                deepest_root_node = deepest_root_node.child

        return deepest_root_node.id
        
    #Helper functions to print
    # def printHeap(self):
    #     if self.root_list is not None:
    #         print()
    #         print("-----------------------------------------------------")
    #         print("|              Fibonacci Heap Structure             |")
    #         print("-----------------------------------------------------")
    #         print()
    #         firstNode = self.root_list
    #         current_node = self.root_list.right
    #         flag = True
    #         while flag:
    #             if current_node == firstNode:
    #                 flag = False
    #             print("|")
    #             if current_node.marked:
    #                 print("---", current_node.value, "+")
    #             else:
    #                 print("---", current_node.value)
    #             if current_node.child is not None:
    #                 self.recursivePrint(current_node, 1)
    #             current_node = current_node.right
    #             print()
    # def recursivePrint(self, node, degree):
    #     firstNode = node.child
    #     current_node = node.child.right
    #     flag = True
    #     s = "  "

    #     while flag:
    #         if current_node == firstNode:
    #             flag = False
    #         print(s*degree, "|")
    #         if current_node.marked:
    #             print(s*degree, "---", current_node.value, "+")
    #         else: 
    #             print(s*degree, "---", current_node.value)
    #         if current_node.child is not None:
    #             self.recursivePrint(current_node, degree+2)
    #         current_node = current_node.right
