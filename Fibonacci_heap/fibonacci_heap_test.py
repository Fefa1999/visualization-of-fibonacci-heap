import unittest
from FibonacciHeap import FibonacciHeap
# python3 -m unittest fibonacci_heap_test.py

class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.heap = FibonacciHeap()
    
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
    
    def test_merge_heaps_empty_with_non_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap2.insert(5)
        heap2.insert(6)
        heap2.insert(7)
        self.assertEqual(heap1.min_fib_node, None, "Heap should be empty")
        self.assertEqual(heap1.root_list, None, "Heap should be empty")
        self.assertEqual(heap1.total_fib_nodes, 0, "Heap should be empty")
        heap1.merge_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "After merge, the new min should be 5")
        self.assertEqual(heap1.root_list.value, 5, "The root list should be 5")
        self.assertEqual(heap1.total_fib_nodes, 3, "Heap should consist of 3 nodes")

    def test_merge_heaps_non_empty_with_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(5)
        heap1.insert(6)
        heap1.insert(7)
        old_min = heap1.min_fib_node.value
        old_root = heap1.root_list.value
        length = heap1.total_fib_nodes
        heap1.merge_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, old_min, "The heap values should not change")
        self.assertEqual(heap1.root_list.value, old_root, "The heap values should not change")
        self.assertEqual(heap1.total_fib_nodes, length, "The heap values should not change")

    def test_merge_heaps_both_non_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(10)
        heap2.insert(5)
        heap1.merge_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "The heap min should be 5")
        self.assertEqual(heap1.total_fib_nodes, 2, "The total nodes should be 2")

    def test_merge_heaps_both_non_empty(self):
        heap1 = FibonacciHeap()
        heap2 = FibonacciHeap()
        heap1.insert(10)
        heap1.insert(11)
        heap1.insert(12)
        heap2.insert(5)
        heap2.insert(6)
        heap2.insert(7)
        heap1.merge_heaps(heap2)
        self.assertEqual(heap1.min_fib_node.value, 5, "The new min node should be 5")
        self.assertEqual(heap1.total_fib_nodes, 6, "The new total nodes should be 6")

    
if __name__ == '__main__':
    unittest.main()