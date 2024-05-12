from FibonacciHeap import FibonacciHeap
import time
import matplotlib.pyplot as plt
import numpy as np

def measure_extract_min_time(heap_size):
    heap = FibonacciHeap()
    for i in range(heap_size):
        heap.insert(i)

    start = time.time()*1000000
    for i in range(heap_size):
        heap.extract_min()
    end = time.time()*1000000
    return (end - start)/heap_size

def measure_decrease_key_time(heap_size):
    heap = FibonacciHeap()
    for i in range(heap_size):
        heap.insert(i)
    heap.extract_min()
    
    times = []
    current_child = heap.root_list
    while True:
        if current_child.child.left == current_child.child:
            large_start = time.time()*1000000
            heap.decrease_value(current_child.child, -1*current_child.child.value)
            large_end = time.time()*1000000
            times.append(large_end-large_start)
            break
        
        current_child = current_child.child.left
        start = time.time()*1000000
        heap.decrease_value(current_child.child, -1*current_child.child.value)
        end = time.time()*1000000
        times.append(end-start)

    acc_time = 0
    for t in times:
        acc_time += t
        
    return acc_time/len(times)

def measure_insert_time(heap_size, repeat):
    heap = FibonacciHeap()
    t = 0
    for i in range(repeat):
        for i in range(heap_size):
            heap.insert(i)

        start = time.time()*1000000
        heap.insert(0)
        end = time.time()*1000000
        t += end-start
    return t/repeat

def measure_meld_time(heap_size):
    heap_one = FibonacciHeap()
    heap_two = FibonacciHeap()

    for i in range(heap_size):
        heap_one.insert(i)
        heap_two.insert(i)
    
    start = time.time()*1000000
    heap_one.meld_heaps(heap_two)
    end = time.time()*1000000

    return end-start

def plot_all():
    t = time.time()
    repeat = 1
    # Approx 10 minutes
    extract_sizes = [10, 100, 1000, 10000, 100000, 1000000, 2000000, 4000000, 6000000, 8000000, 10000000]
    extract_times = [measure_extract_min_time(size) for size in extract_sizes]
    extract_sizes = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 2, 4, 6, 8, 10]
    time_one = time.time()-t
    print("done 1 in:", time_one)
    # Approx 1 minute
    dc_sizes = [524289, 1048577, 2097153, 4194305, 8388609]
    dc_times = [measure_decrease_key_time(size) for size in dc_sizes]
    dc_sizes = [0.524289, 1.048577, 2.097153, 4.194305, 8.388609]
    time_two = time.time()-t
    print("done 2 in:", time_two-time_one)
    # Approx 2 minutes
    insert_sizes = [100, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]
    insert_times = [measure_insert_time(size, repeat) for size in insert_sizes]
    insert_sizes = [0.0001, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    time_three = time.time()-t
    print("done 3 in:", time_three-time_two)
    # Approx 4 minutes
    meld_sizes = [100, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]
    meld_times = [measure_meld_time(size) for size in meld_sizes]
    meld_sizes = [0.0001, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    time_four = time.time()-t
    print("done 4 in:", time_four-time_three)

    plt.plot(extract_sizes, extract_times, marker='o', linestyle='-', color='b', label='extract min')
    plt.plot(dc_sizes, dc_times, marker='o', linestyle='-', color='r', label='decrease key')
    plt.plot(insert_sizes, insert_times, marker='o', linestyle='-', color='g', label='insert')
    plt.plot(meld_sizes, meld_times, marker='o', linestyle='-', color='y', label='meld')

    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Heap Size (nodes) in million')
    plt.ylabel('Time in microsecond')
    plt.title('Operation Performance - Red: decrease key - Blue: extract min - Green: insert - Yellow: meld')
    plt.grid(True)
    plt.show()

plot_all()