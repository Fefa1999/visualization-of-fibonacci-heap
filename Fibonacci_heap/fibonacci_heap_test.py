import unittest
from FibonacciHeap import FibonacciHeap
# python3 -m unittest fibonacci_heap_test.py
# coverage run --omit "/Users/felixfatum/Library/Python/3.10/lib/python/site-packages/_distutils_hack/__init__.py" fibonacci_heap_test.py
# coverage html
# open htmlcov/index.html

class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.heap = FibonacciHeap()
    
    #INSERT TESTING
    def test_insert_single(self):
        node, updated = self.heap.insert(10)
        self.assertEqual(node.value, 10, "Check that the value is correct")
        self.assertTrue(updated, "Should return True since min node has been updated")
        self.assertEqual(self.heap.min_fib_node, node, "Inserted node should be the min node")
        self.assertEqual(self.heap.root_list, node, "Inserted node should be the root_list entry point")
    
    def test_insert_multiple(self):
        nodes = [self.heap.insert(i)[0] for i in range(10, 0, -1)]
        self.assertEqual(self.heap.min_fib_node.value, 1, "The new minimum node should have the value 1")
        self.assertEqual(self.heap.total_fib_nodes, 10, "Checks the total nodes")

    def test_insert_in_heaps_double_circular_linked_list_property_maintained(self):
        heap1 = FibonacciHeap()
        heap1.insert(10)
        self.assertEqual(heap1.root_list.value, 10, "The first node in the root list should be 10")
        heap1.insert(11)
        self.assertEqual(heap1.root_list.value, 10, "The first node in the root list should be 10")
        self.assertEqual(heap1.root_list.right.value, 11, "The next node in the root list should be 11")
        self.assertEqual(heap1.root_list.right.right.value, 10, "The next node in the root list should be 10 as it circles back")
        heap1.insert(12)
        self.assertEqual(heap1.root_list.value, 10, "The first item in the root list should be 10")
        self.assertEqual(heap1.root_list.right.value, 11, "The first item in the root list should be 10")
        self.assertEqual(heap1.root_list.right.right.value, 12, "The first item in the root list should be 10")
        self.assertEqual(heap1.root_list.right.right.right.value, 10, "The next node in the root list should be 10 as it circles back")
    
    # UPDATE MIN SINGLE NODE TESTING
    def test_update_min_with_single_node_lower_value(self):
        self.heap.insert(10)
        new_node = FibonacciHeap.FibonacciHeapNode(5, 1)
        updated = self.heap.update_min_with_single_node(new_node)
        self.assertTrue(updated, "Should return True since new min has been inserted")
        self.assertEqual(self.heap.min_fib_node.value, 5, "The new min node should be 5")
    
    def test_update_min_with_single_node_higher_value(self):
        self.heap.insert(10)
        new_node = FibonacciHeap.FibonacciHeapNode(20, 1)
        updated = self.heap.update_min_with_single_node(new_node)
        self.assertFalse(updated, "Should return False, since the min hasn't been changed")
        self.assertEqual(self.heap.min_fib_node.value, 10, "Unchanged min node")
    
    def test_update_min_with_single_node_same_value(self):
        self.heap.insert(10)
        new_node = FibonacciHeap.FibonacciHeapNode(10, 1)
        updated = self.heap.update_min_with_single_node(new_node)
        self.assertTrue(updated, "Should return True, since the min has been changed")
        self.assertEqual(self.heap.min_fib_node.value, 10, "new min node, same value")

    # UPDATE FROM ROOT LIST TESTING - no need to test with empty heap since function will only be called with non empty heap
    def test_set_new_min_from_root_list_multiple_nodes_in_root(self):
        self.heap.insert(12)
        self.heap.insert(2)
        self.heap.insert(400)
        self.heap.insert(9)
        self.heap.min_fib_node = None
        self.assertIsNone(self.heap.min_fib_node)
        self.heap.set_new_min_from_root_list()
        self.assertEqual(self.heap.min_fib_node.value, 2)
    
    def test_set_new_min_from_root_list_single_node_in_root(self):
        self.heap.insert(12)
        self.heap.min_fib_node = None
        self.assertIsNone(self.heap.min_fib_node)
        self.heap.set_new_min_from_root_list()
        self.assertEqual(self.heap.min_fib_node.value, 12)

    # RETURN MIN TESTING 
    def test_return_min_total_nodes_above_one(self):
        self.heap.insert(12)
        self.heap.insert(2)
        self.heap.insert(400)
        self.heap.insert(9)
        min_node = self.heap.return_min()
        self.assertEqual(min_node.value, 2)
    
    def test_return_min_total_nodes_exactly_one(self):
        self.heap.insert(12)
        min_node = self.heap.return_min()
        self.assertEqual(min_node.value, 12)
    
    def test_return_min_total_empty_heap(self):
        min_node = self.heap.return_min()
        self.assertIsNone(min_node)

    #MELD HEAPS TESTING
    def test_meld_heaps_empty_with_non_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap2.insert(5)
        heap2.insert(6)
        heap2.insert(7)
        self.assertEqual(heap1.min_fib_node, None, "Heap should be empty")
        self.assertEqual(heap1.root_list, None, "Heap should be empty")
        self.assertEqual(heap1.total_fib_nodes, 0, "Heap should be empty")
        heap1.meld_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "After meld, the new min should be 5")
        self.assertEqual(heap1.root_list.value, 5, "The root list should be 5")
        self.assertEqual(heap1.total_fib_nodes, 3, "Heap should consist of 3 nodes")

    def test_meld_heaps_non_empty_with_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(5)
        heap1.insert(6)
        heap1.insert(7)
        old_min = heap1.min_fib_node.value
        old_root = heap1.root_list.value
        length = heap1.total_fib_nodes
        heap1.meld_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, old_min, "The heap values should not change")
        self.assertEqual(heap1.root_list.value, old_root, "The heap values should not change")
        self.assertEqual(heap1.total_fib_nodes, length, "The heap values should not change")

    def test_meld_heaps_both_non_empty_single_nodes(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(10)
        heap2.insert(5)
        heap1.meld_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "The heap min should be 5")
        self.assertEqual(heap1.total_fib_nodes, 2, "The total nodes should be 2")

    def test_meld_heaps_both_non_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(10)
        heap1.insert(11)
        heap1.insert(12)
        heap2.insert(5)
        heap2.insert(6)
        heap2.insert(7)
        heap1.meld_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "The new min node should be 5")
        self.assertEqual(heap1.total_fib_nodes, 6, "The new total nodes should be 6")

    #MELD INTO ROOT TESTING 
    def test_meld_into_root_list_non_empty_root_list(self):
        self.heap.insert(2)
        self.heap.insert(4)
        new_node = FibonacciHeap.FibonacciHeapNode(20, 1)
        self.heap.meld_node_into_root_list(new_node)
        self.assertEqual(self.heap.root_list.right.right.value, 20)
        self.assertEqual(self.heap.root_list.left.value, 20)
        self.assertEqual(self.heap.root_list.right.right.right.value, 2)
        self.assertEqual(self.heap.root_list.right.right.left.value, 4)
        self.assertEqual(self.heap.root_list.value, 2)
    
    def test_meld_into_root_list_empty_root_list(self):
        new_node = FibonacciHeap.FibonacciHeapNode(20, 1)
        self.heap.meld_node_into_root_list(new_node)
        self.assertEqual(self.heap.root_list.value, 20)
    
    # REMOVE NODE FROM ROOT LIST TESTING 
    def test_remove_node_from_root_list_size_above_one(self):
        self.heap.insert(2)
        self.heap.insert(4)
        node = self.heap.insert(6)
        self.heap.remove_node_from_root_list(node[0])
        self.assertEqual(self.heap.root_list.value, 2)
        self.assertEqual(self.heap.root_list.right.value, 4)
        self.assertEqual(self.heap.root_list.right.right.value, 2)
    
    def test_remove_node_from_root_list_size_exactly_one(self):
        node = self.heap.insert(6)
        self.heap.remove_node_from_root_list(node[0])
        self.assertIsNone(self.heap.root_list)
        self.assertIsNone(self.heap.min_fib_node)

    # MELD INTO CHILD LIST TESTING 
    def test_meld_into_child_list_non_empty_child_list(self):
        self.heap.insert(2)
        parent = self.heap.insert(4)
        self.heap.insert(6)
        self.heap.insert(8)
        self.heap.insert(10)
        child = FibonacciHeap.FibonacciHeapNode(20, 1)
        self.heap.extract_min()
        self.heap.meld_node_into_child_list(child, parent[0])
        self.assertEqual(self.heap.root_list.child.value, 6)
        self.assertEqual(self.heap.root_list.child.left.value, 20)
        self.assertEqual(self.heap.root_list.child.right.value, 8)
        self.assertEqual(self.heap.root_list.child.right.right.value, 20)
    
    def test_meld_into_child_list_empty_child_list(self):
        parent = self.heap.insert(1)
        child = FibonacciHeap.FibonacciHeapNode(20, 1)
        self.heap.meld_node_into_child_list(child, parent[0])
        self.assertEqual(self.heap.root_list.child.value, 20)
        self.assertEqual(self.heap.root_list.child.right.value, 20)
        self.assertEqual(self.heap.root_list.child.left.value, 20)
    
    # REMOVE NODE FROM CHILD LIST - No need to test empty child list since this wont be called
    def test_remove_node_from_child_list_above_one_child(self):
        self.heap.insert(2)
        self.heap.insert(4)
        self.heap.insert(6)
        child = self.heap.insert(8)
        self.heap.insert(10)
        self.heap.extract_min()
        self.heap.remove_node_from_child_list(child[0])
        self.assertEqual(self.heap.root_list.child.value, 6)
        self.assertEqual(self.heap.root_list.child.left.value, 6)
        self.assertEqual(self.heap.root_list.child.right.value, 6)
    
    def test_remove_node_from_child_list_exactly_one_child(self):
        self.heap.insert(2)
        self.heap.insert(4)
        child = self.heap.insert(6)
        self.heap.extract_min()
        self.heap.remove_node_from_child_list(child[0])
        self.assertIsNone(self.heap.root_list.child)

    # # EXTRACT MIN TESTING
    def test_extract_min_from_empty_heap(self):
        min_node = self.heap.extract_min()
        self.assertIsNone(min_node, "Should return None if heap is empty")

    def test_extract_min_from_heap_size_1(self):
        self.heap.insert(1)
        min_node, actions, new_min = self.heap.extract_min()
        self.assertEqual(min_node.value, 1)
        self.assertIsNone(self.heap.root_list)
        self.assertIsNone(self.heap.min_fib_node)
        self.assertIsNone(new_min)
        self.assertEqual(len(actions), 0, "No linking steps needed")

    def test_extract_min_from_heap_size_2_with_only_one_root(self):
        self.heap.insert(1)
        self.heap.insert(2)
        self.heap.insert(0)
        self.heap.extract_min()

        min_node, actions, new_min = self.heap.extract_min()
        self.assertEqual(min_node.value, 1)
        self.assertEqual(self.heap.root_list.value, 2)
        self.assertEqual(self.heap.min_fib_node.value, 2)
        self.assertEqual(new_min.value, 2)
        self.assertEqual(len(actions), 0, "No linking steps needed")

    def test_extract_min_single_root_with_multiple_children(self):
        for i in range(9):
            self.heap.insert(i)
        
        self.heap.extract_min()
        self.heap.extract_min()
        
        self.assertEqual(self.heap.root_list.value, 2)
        self.assertEqual(self.heap.root_list.right.value, 3)
        self.assertEqual(self.heap.root_list.right.right.value, 5)

    def test_extract_min_with_5_len_root_list(self):
        self.heap.insert(10)
        self.heap.insert(5)
        self.heap.insert(1)
        self.heap.insert(3)
        self.heap.insert(15)
        min_node, actions, new_min = self.heap.extract_min()
        self.assertEqual(min_node.value, 1, "Min value node extracted")
        self.assertEqual(new_min.value, 3, "The new minimum node should be 3")
        #After consolidation the heap should consist of one root with 2 children, with one of the children having a further child
        self.assertEqual(self.heap.root_list.value, 3)
        self.assertEqual(self.heap.root_list.child.value, 15)
        self.assertEqual(self.heap.root_list.child.right.value, 5)
        self.assertEqual(self.heap.root_list.child.right.child.value, 10)
        self.assertEqual(len(actions), 3, "Three linking steps involved")

    # CONSOLIDATE TESTING - No need to test empty heap or heap with root size one, since it wont happen
    def test_consolidate(self):
        self.heap.insert(1)
        self.heap.insert(2)
        self.heap.insert(3)
        self.heap.insert(4)
        actions = self.heap.consolidate()
        self.assertEqual(len(actions), 3, "Three linkings made - 4 under 3, 2 under 1 and 3 under 1")
        # CHECK LINKING IS DONE CORRECT
        self.assertEqual(self.heap.root_list.value, 1, "Root stays as 1")
        self.assertEqual(self.heap.root_list.child.value, 2, "First child of root")
        self.assertEqual(self.heap.root_list.child.right.value, 3, "Second child of root")
        self.assertEqual(self.heap.root_list.child.right.child.value, 4, "child of second child of root")

    # LINK NODES TESTING 
    def test_link_nodes(self):
        child, update = self.heap.insert(3)
        parent, update = self.heap.insert(2)
        self.heap.link_nodes(child, parent)
        self.assertEqual(parent.child.value, 3)
        self.assertEqual(child.parent.value, 2)
        self.assertEqual(parent.degree, 1)
        self.assertEqual(self.heap.root_list.value, 2)
        self.assertEqual(self.heap.root_list.right.value, 2)
    
    def test_link_nodes_same_value(self):
        child, update = self.heap.insert(2)
        parent, update = self.heap.insert(2)
        self.heap.link_nodes(child, parent)
        self.assertEqual(parent.child.value, 2)
        self.assertEqual(child.parent.value, 2)
        self.assertEqual(parent.degree, 1)
    
    def test_link_nodes_with_marked_node(self):
        child, update = self.heap.insert(2)
        child.marked = True
        parent, update = self.heap.insert(1)
        self.heap.link_nodes(child, parent)
        self.assertEqual(parent.child.value, 2)
        self.assertFalse(child.marked)
        self.assertEqual(child.parent.value, 1)
        self.assertEqual(parent.degree, 1)

    # DECREASE VALUE TEST 
    def test_decrease_value_single_node_heap(self):
        node, update = self.heap.insert(10)
        self.heap.decrease_value(node, 1)
        self.assertEqual(node.value, 1, "New value after decreasing")

    def test_decrease_value_value_higher_than_node_value(self):
        node, update = self.heap.insert(10)
        self.heap.decrease_value(node, 100)
        self.assertEqual(node.value, 10, "Should stay unchanged")

    def test_decrease_value_value_lower_than_node_value_and_higher_than_parent(self):
        self.heap.insert(10)
        node, update = self.heap.insert(30)
        self.heap.insert(20)
        self.heap.extract_min()
        self.heap.decrease_value(node, 25)
        self.assertEqual(self.heap.root_list.value, 20)
        self.assertEqual(self.heap.root_list.right.value, 20)
        self.assertEqual(self.heap.root_list.child.value, 25, "Should remain child, but value changed")

    def test_decrease_value_value_lower_than_node_value_and_lower_than_parent(self):
        self.heap.insert(10)
        node, update = self.heap.insert(30)
        self.heap.insert(20)
        self.heap.extract_min()
        self.heap.decrease_value(node, 2)
        self.assertEqual(self.heap.root_list.value, 20)
        self.assertEqual(self.heap.root_list.right.value, 2, "The node decreased has been cut and added to root list since it violates the heap property")
        self.assertIsNone(self.heap.root_list.child)

    def test_decrease_value_with_cut_and_cascading_cut(self):
        for i in range(17):
            if i == 10:
                node_ten, u = self.heap.insert(i)
            elif i == 14:
                node_fourteen, u =self.heap.insert(i)
            elif i == 15:
                node_fifteen, u =self.heap.insert(i)
            else:
                self.heap.insert(i)
        
        self.heap.extract_min()
        self.heap.decrease_value(node_ten, -10)
        self.heap.decrease_value(node_fourteen, -14)
        self.heap.decrease_value(node_fifteen, -15)

        #AFTER THE LAST DECREASE VALUE WE SHOULD HAVE 6 ROOTS, original root, 3 through cuts and 2 thorugh cascading cuts

        #Original root
        self.assertEqual(self.heap.root_list.value, 1)
        self.assertEqual(self.heap.root_list.degree, 3)

        #First Cut 
        self.assertEqual(self.heap.root_list.right.value, -10)
        self.assertEqual(self.heap.root_list.right.degree, 0)

        #Second Cut
        self.assertEqual(self.heap.root_list.right.right.value, -14)
        self.assertEqual(self.heap.root_list.right.right.degree, 0)

        #Third Cut
        self.assertEqual(self.heap.root_list.right.right.right.value, -15)
        self.assertEqual(self.heap.root_list.right.right.right.degree, 1)

        #First cascading cut 
        self.assertEqual(self.heap.root_list.right.right.right.right.value, 13)
        self.assertEqual(self.heap.root_list.right.right.right.right.degree, 0)

        #Second cascading cut 
        self.assertEqual(self.heap.root_list.right.right.right.right.right.value, 9)
        self.assertEqual(self.heap.root_list.right.right.right.right.right.degree, 1)

if __name__ == '__main__':
    unittest.main()