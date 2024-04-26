import math 
import time
class FibonacciHeap:
    root_list = None
    min_fib_node = None
    total_fib_nodes = 0
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
        new_node = self.FibonacciHeapNode(value, self.id)
        new_heap = FibonacciHeap()
        new_heap.total_fib_nodes = 1
        new_heap.min_fib_node = new_heap.root_list = new_node
        update = self.merge_heaps(new_heap)
        self.id += 1
        return (new_node, update)

    #updates min if node is smaller than current min
    def update_min_with_single_node(self, fib_node):
        if self.min_fib_node is None or fib_node.value <= self.min_fib_node.value:
            self.min_fib_node = fib_node
            return True
        else: 
            return False
   
    #iterates the circular doubly linked list and updates min node
    def set_new_min_from_root_list(self):
        current_node = self.root_list.right
        while True: 
            self.update_min_with_single_node(current_node)
            if self.root_list == current_node:
                break
            current_node = current_node.right

    #return min node in O(1) time
    def return_min(self):
        return self.min_fib_node

    #Merge two heaps by appending nodes to root list of first heap
    def merge_heaps(self, heap_two):
        if self.root_list is None and heap_two.root_list is not None:
            self.root_list = heap_two.root_list
            self.min_fib_node = heap_two.min_fib_node
            self.total_fib_nodes = heap_two.total_fib_nodes
            return True
        elif self.root_list is not None and heap_two.root_list is not None:
            new_end = heap_two.root_list.left
            self.root_list.left.right = heap_two.root_list
            heap_two.root_list.left.right = self.root_list
            heap_two.root_list.left = self.root_list.left
            self.root_list.left = new_end
            self.total_fib_nodes += heap_two.total_fib_nodes 
            return self.update_min_with_single_node(heap_two.min_fib_node)

    # insert a node in the circular doubly linked list root_list - will be inserted as new root  
    def meld_node_into_root_list(self, node_to_insert):
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
    def meld_node_into_child_list(self, fib_node_child, fib_node_parent):
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
                    self.cut(current_child)
                    if min_node.child is None:
                        break
                    current_child = next_child

            #set new min to next 
            self.min_fib_node = min_node.right

            #remove min node from root
            self.remove_node_from_root_list(min_node)
            self.total_fib_nodes -= 1
            actions = []
            #Consolidate and set new min unless root_list is only one root or empty - the only child of the removed min
            if self.root_list is not None:
                if self.root_list != self.root_list.right:
                    actions = self.consolidate()
                self.set_new_min_from_root_list()
            return (min_node, actions, self.min_fib_node)

    #Map heap until no root has same degree
    def consolidate(self):
        actions = []
        max_degree = int(math.log(self.total_fib_nodes, (1 + math.sqrt(5)) / 2)) 
        array = [None] * (max_degree + 1)
        # if self.scene is not None:
        #     scene_array = self.scene.create_array((max_degree + 1), self.showExplanatoryText)
        array[self.root_list.degree] = self.root_list
        # if self.scene is not None:
        #     self.scene.add_number_to_empty_space_in_array(self.root_list.degree, self.root_list.id, scene_array, self.showExplanatoryText, True)
        end_node = self.root_list.left
        current_node = self.root_list.right

        while True: 
            next_node = current_node.right
            if array[current_node.degree] is None:
                array[current_node.degree] = current_node
                # if self.scene is not None:
                #     self.scene.add_number_to_empty_space_in_array(current_node.degree, current_node.id, scene_array, self.showExplanatoryText, False)
            else:
                nodes = self.link_nodes(array[current_node.degree], current_node)
                node = nodes[0]
                actions.append((nodes[0], nodes[1]))
                array[node.degree-1] = None
                # if self.scene is not None:
                #     self.scene.remove_from_array(node.degree-1, scene_array, self.showExplanatoryText)
                while node.degree <= max_degree-1 and array[node.degree] is not None:
                    nodes = self.link_nodes(array[node.degree], node)
                    node = nodes[0]
                    actions.append((nodes[0], nodes[1]))
                    array[node.degree-1] = None
                    # if self.scene is not None:
                    #     self.scene.remove_from_array(node.degree-1, scene_array, self.showExplanatoryText)
                array[node.degree] = node
                # if self.scene is not None:
                #     self.scene.add_number_to_filled_space_in_array(node.degree, node.id, scene_array, self.showExplanatoryText)
            if current_node == end_node:
                # if self.scene is not None:
                #     self.scene.remove_array(scene_array, self.showExplanatoryText)
                break
            current_node = next_node

        return actions

    #Link two nodes together - one will become child, other parent 
    def link_nodes(self, fib_node_one, fib_node_two):
            fib_node_child = fib_node_one if fib_node_one.value >= fib_node_two.value else fib_node_two
            fib_node_parent = fib_node_one if fib_node_two.value > fib_node_one.value else fib_node_two
            self.remove_node_from_root_list(fib_node_child)
            self.meld_node_into_child_list(fib_node_child, fib_node_parent)
            fib_node_child.parent = fib_node_parent
            fib_node_parent.degree += 1
            return (fib_node_parent, fib_node_child)

    #function to decrease value of a node - eg. 46 -> 12 
    def decrease_value(self, node_to_decrease, new_value):
        if node_to_decrease.value > new_value:
            node_to_decrease.value = new_value
            parent = node_to_decrease.parent
            actions = []
            if parent is not None and parent.value > new_value:
                cut_node_info = self.cut(node_to_decrease)
                actions.append(cut_node_info)
                actions = self.cascading_cut(parent, actions)

            update = self.update_min_with_single_node(node_to_decrease) 
            return (True, node_to_decrease, actions, update)
        else:
            return (False, node_to_decrease, new_value)

    #Cut node from child list to root 
    def cut(self, node_to_cut):
        self.remove_node_from_child_list(node_to_cut)
        self.meld_node_into_root_list(node_to_cut)
        mark = node_to_cut.marked
        if node_to_cut.marked:
            node_to_cut.marked = False
        return (node_to_cut, mark)
        
    # handle parent of cut node in decreasing a value
    def cascading_cut(self, decreased_node_parent, actions):
        if decreased_node_parent.parent is not None:
            if not decreased_node_parent.marked:
                decreased_node_parent.marked = True
                actions.append(decreased_node_parent)
                return actions
            else:
                next_parent = decreased_node_parent.parent
                cut_node_info = self.cut(decreased_node_parent)
                actions.append(cut_node_info)
                self.cascading_cut(next_parent, actions)
                return actions
        else:
            return actions

    def delete_node(self, node_to_delete):
        self.decrease_value(node_to_delete, -float('inf'))
        self.extract_min() 
    
    def increaseKey(self, node_to_increase, value):
        self.decrease_value(node_to_increase, -float('inf'))
        self.extract_min()
        self.insert(value)
        
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

# def run():
#     heap = FibonacciHeap()
#     print("--------------------")
    
#     for i in range(333):
#         if i == 123:
#             x = heap.real_insert(i)
#         else:
#             heap.insert(i)
    
#     heap.extract_min()
    
#     heap.printHeap()
# run()