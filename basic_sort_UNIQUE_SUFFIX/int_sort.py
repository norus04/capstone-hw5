# =========================================================================
#
#  Copyright Ziv Yaniv
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =========================================================================

"""
This module sorts lists of integers...
"""
import os
import psutil
import time


def bubble(int_list):
    """
    Perform bubble sort on a list of integers.

    Parameters
    ----------
    int_list : list[int]
        A list of integers to be sorted.

    Returns
    -------
    list[int]
        A new sorted list of integers.

    Notes
    -----
    Bubble sort is a simple sorting algorithm that repeatedly steps through
    the list, compares adjacent elements and swaps them if they are in the
    wrong order.
    """
    # Create a copy to avoid mutating the original list
    arr = int_list.copy()
    n = len(arr)

    for i in range(n):
        # Flag to optimize by breaking early if no swaps occur
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no swapping occurred, array is already sorted
        if not swapped:
            break

    return arr


def measure_bubble_cpu(int_list, runs=1):
    """
    Measure CPU usage while performing bubble sort.

    Parameters
    ----------
    int_list : list[int]
        Data to sort.
    runs : int, optional
        Number of times to run bubble sort for averaging. Default is 1.

    Returns
    -------
    dict
        {
          "sorted": <sorted list from last run>,
          "avg_cpu_time": <average total CPU time>,
          "avg_rss_bytes": <average memory usage change>
        }
    """
    process = psutil.Process(os.getpid())

    # Lists to store measurement results
    total_times = []
    rss_changes = []
    sorted_out = None

    for _ in range(runs):
        # Record the start time and initial memory
        start_time = time.time()
        before_rss = process.memory_info().rss

        # Perform the sort
        sorted_out = bubble(int_list)

        # Record end time and memory
        end_time = time.time()
        after_rss = process.memory_info().rss

        # Store results
        total_times.append(end_time - start_time)
        rss_changes.append(after_rss - before_rss)

    # Calculate averages
    avg_total_time = sum(total_times) / len(total_times)
    avg_rss_change = sum(rss_changes) / len(rss_changes)

    return {
        "sorted": sorted_out,
        "avg_cpu_time": avg_total_time,
        "avg_rss_bytes": avg_rss_change,
    }


def quick(int_list):
    """
    Sort a list of integers using the Quick Sort algorithm.

    Parameters
    ----------
    int_list : list[int]
        A list of integers to be sorted.

    Returns
    -------
    list[int]
        A new sorted list of integers.

    Notes
    -----
    This implementation is recursive and does not mutate the input list.
    It uses a middle pivot and partitions the list into three groups:
    values less than the pivot, equal to the pivot, and greater than
    the pivot.
    """
    # Base case: empty or single-element list is already sorted
    if len(int_list) <= 1:
        return int_list.copy()

    # Use a pivot (middle element)
    pivot = int_list[len(int_list) // 2]

    # Partition into three lists
    left = [x for x in int_list if x < pivot]
    middle = [x for x in int_list if x == pivot]
    right = [x for x in int_list if x > pivot]

    # Recursively sort left and right, concatenate
    return quick(left) + middle + quick(right)


def measure_quick_cpu(int_list, runs=1):
    """
    Measure CPU time and memory usage while running quick sort.

    Parameters
    ----------
    int_list : list[int]
        Data to sort.
    runs : int, optional
        Number of times to run quick sort for averaging.

    Returns
    -------
    dict
        {
          "sorted": <sorted output from last run>,
          "avg_cpu_time": <average runtime in seconds>,
          "avg_rss_bytes": <average change in memory usage in bytes>
        }
    """
    process = psutil.Process(os.getpid())
    total_times = []
    rss_changes = []
    sorted_out = None

    for _ in range(runs):
        before_rss = process.memory_info().rss
        start = time.time()

        sorted_out = quick(int_list)

        end = time.time()
        after_rss = process.memory_info().rss

        total_times.append(end - start)
        rss_changes.append(after_rss - before_rss)

    avg_time = sum(total_times) / len(total_times)
    avg_rss = sum(rss_changes) / len(rss_changes)

    return {"sorted": sorted_out, "avg_cpu_time": avg_time, "avg_rss_bytes": avg_rss}


def insertion(int_list):
    """
    This function sorts a list of integers using insertion sort.

    Parameters
    ----------
    int_list : list[int]
        A list of integers.

    Returns
    -------
    list[int]
        A new list containing the sorted integers.

    Notes
    -----
    Insertion sort is an in-place, stable sorting algorithm.
    In this implementation we copy the list first so that
    the original data is not mutated (important for testing).
    """

    arr = int_list.copy()  # Copy to avoid mutating caller’s list

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Shift larger elements right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def measure_insertion_memory(int_list, runs=1):
    """
    This function measures memory usage (resident set size change)
    while running insertion sort.

    Parameters
    ----------
    int_list : list[int]
        Data to sort.
    runs : int, optional
        Number of times to run insertion for averaging.

    Returns
    -------
    dict
        {
          "sorted": <sorted list from last run>,
          "avg_rss_bytes": <average RSS increase in bytes>
        }
    """
    process = psutil.Process(os.getpid())
    changes = []
    sorted_out = None

    for _ in range(runs):
        before = process.memory_info().rss
        sorted_out = insertion(int_list)
        after = process.memory_info().rss
        changes.append(after - before)

    average_change = sum(changes) / len(changes) if changes else 0
    after_rss = process.memory_info().rss

    return {
        "sorted": sorted_out,
        "avg_rss_bytes": average_change,
        "after_rss_bytes": after_rss,
    }
