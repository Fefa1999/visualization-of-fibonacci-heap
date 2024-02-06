import unittest
import FibonacciHeap

class TestFibonacciHeap(unittest.TestCase):
    def setUp(self):
        self.heap = FibonacciHeap.FibonacciHeap()
    
    def test_insert(self):
        self.heap.insert(3)
        self.heap.insert(2)
        self.assertEqual(self.heap.total_fib_nodes, 2, "Total nodes should be 2")
    
    def test_return_min(self):
        self.heap.insert(2)
        self.heap.insert(1)
        self.heap.insert(4)
        min_node = self.heap.returnMin()
        self.assertEqual(min_node.key, 1, "The minimum key should be 1")

    def test_merge_heaps_total_nodes_updated(self):
        self.heap.insert(3)
        self.heap.insert(1)
        self.heap.insert(2)
        heap_1 = FibonacciHeap.FibonacciHeap()
        heap_1.insert(0)
        heap_1.insert(4)
        heap_1.insert(5)
        self.heap.merge_heaps(heap_1)
        self.assertEqual(self.heap.total_fib_nodes, 6, "Total nodes after merge should be 6")

    def test_merge_heaps_new_min_updated(self):
        self.heap.insert(3)
        self.heap.insert(1)
        self.heap.insert(2)
        heap_1 = FibonacciHeap.FibonacciHeap()
        heap_1.insert(0)
        heap_1.insert(4)
        heap_1.insert(5)
        self.heap.merge_heaps(heap_1)
        self.assertEqual(self.heap.returnMin().key, 0, "Minimum key after merge should be 0")

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
