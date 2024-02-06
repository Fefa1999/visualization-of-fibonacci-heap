import unittest
import FibonacciHeap

class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.heap = FibonacciHeap.FibonacciHeap()
    
    def test_insert(self):
        self.heap.insert(3)
        self.heap.insert(2)
        self.assertEqual(self.heap.total_fib_nodes, 2, "Total nodes should be 2")
    
    def test_merge_node_with_root_list_when_list_is_none(self):
        node = self.heap.FibonacciHeapNode(1)
        self.heap.merge_node_with_root_list(node)
        self.assertEqual(self.heap.root_list, node, "Inserted node should be the root_list entry point")

    def test_merge_node_with_root_list_when_list_is_not_none(self):
        node = self.heap.FibonacciHeapNode(1)
        self.heap.insert(2)
        self.heap.merge_node_with_root_list(node)
        self.assertEqual(self.heap.root_list, node, "Inserted node should be the root_list entry point")
        self.assertEqual(node.right.key, 2, "Circularity maintained in the doubly linked list")
        self.assertEqual(node.left.key, 2, "Circularity maintained in the doubly linked list")
        self.assertEqual(node.right.right.key, 1, "Circularity maintained in the doubly linked list")
        self.assertEqual(node.left.left.key, 1, "Circularity maintained in the doubly linked list")

    def test_check_min_with_single_node(self):
        node = self.heap.FibonacciHeapNode(1)
        self.heap.insert(2)
        self.assertEqual(self.heap.min_fib_node.key, 2, "Min node should be 2 before inserting new node")
        self.heap.check_min_with_single_node(node)
        self.assertEqual(self.heap.min_fib_node.key, 1, "Min node should be 1 after inserting new node")
    
    def test_check_min_with_single_negative_node(self):
        node = self.heap.FibonacciHeapNode(-1)
        self.heap.insert(2)
        self.assertEqual(self.heap.min_fib_node.key, 2, "Min node should be 2 before inserting new node")
        self.heap.check_min_with_single_node(node)
        self.assertEqual(self.heap.min_fib_node.key, -1, "Min node should be 1 after inserting new node")

    def test_set_new_min_from_root_list(self):
        self.heap.insert(9)
        self.heap.insert(21)
        self.heap.insert(33)
        self.heap.insert(17)
        #fake a wrong min_node
        node = self.heap.FibonacciHeapNode(122)
        self.heap.min_fib_node = node
        self.assertEqual(self.heap.min_fib_node.key, 122, "Min node should be 122 after inserting fake min_node")
        self.heap.set_new_min_from_root_list()
        self.assertEqual(self.heap.min_fib_node.key, 9, "Min node should be 9 after running method")

    def test_set_new_min_from_root_list_with_negative_key(self):
        self.heap.insert(-9)
        self.heap.insert(0)
        self.heap.insert(33)
        self.heap.insert(17)
        #fake a wrong min_node
        node = self.heap.FibonacciHeapNode(122)
        self.heap.min_fib_node = node
        self.assertEqual(self.heap.min_fib_node.key, 122, "Min node should be 122 after inserting fake min_node")
        self.heap.set_new_min_from_root_list()
        self.assertEqual(self.heap.min_fib_node.key, -9, "Min node should be -9 after running method")

    def test_return_min(self):
        self.heap.insert(2)
        self.heap.insert(1)
        self.heap.insert(4)
        min_node = self.heap.returnMin()
        self.assertEqual(min_node.key, 1, "The minimum key should be 1")

    def test_merge_heaps(self):
        self.heap.insert(3)
        self.heap.insert(1)
        self.heap.insert(2)
        heap_1 = FibonacciHeap.FibonacciHeap()
        heap_1.insert(0)
        heap_1.insert(4)
        heap_1.insert(5)
        self.heap.merge_heaps(heap_1)
        self.assertEqual(self.heap.total_fib_nodes, 6, "Total nodes after merge should be 6")
        self.assertEqual(self.heap.returnMin().key, 0, "Minimum node key after merge should be 0")
        self.assertEqual(heap_1.root_list, None, "Other heap should be empty")

    def test_remove_node_from_root_list(self):
        self.heap.insert(1)
        node = self.heap.insert(2)
        self.heap.insert(3)
        self.heap.remove_node_from_root_list(node)
        self.assertEqual(self.heap.root_list.right.right, self.heap.root_list, "root list size should be 2 - two moves to the right in the linked list should be itself")

    def test_remove_node_from_root_list_as_last_node(self):
        node = self.heap.insert(2)
        self.heap.remove_node_from_root_list(node)
        self.assertEqual(self.heap.root_list, None, "root_list should be None")
        self.assertEqual(self.heap.min_fib_node, None, "Min fib node should be None")

    def test_extract_min_extracts_correct_min(self):
        self.heap.insert(3)
        self.heap.insert(2)
        self.heap.insert(1)
        self.heap.insert(17)
        self.heap.insert(223)
        min_node = self.heap.extract_min()
        self.assertEqual(min_node.key, 1, "Extracted minimum key should be 1")

    def test_extract_min_sets_correct_total_nodes(self):
        self.heap.insert(3)
        self.heap.insert(2)
        self.heap.insert(1)
        self.heap.extract_min()
        self.assertEqual(self.heap.total_fib_nodes, 2, "Total nodes should be 2")
        self.heap.extract_min()
        self.assertEqual(self.heap.total_fib_nodes, 1, "Total nodes should be 1")
        self.heap.extract_min()
        self.assertEqual(self.heap.total_fib_nodes, 0, "Total nodes should be 0")
    
    def test_extract_min_with_empty_heap(self):
        node = self.heap.extract_min()
        self.assertEqual(node, None, "return should be None")

    def test_decrease_key(self):
        node = self.heap.insert(3)
        self.heap.insert(2)
        self.heap.decrease_key(node, 1)
        self.assertEqual(self.heap.returnMin().key, 1, "Minimum key after decreasing should be 1")

if __name__ == '__main__':
    unittest.main()
