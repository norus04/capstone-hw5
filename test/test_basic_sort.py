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

import pytest
import numpy as np
from basic_sort_UNIQUE_SUFFIX.int_sort import insertion
from basic_sort_UNIQUE_SUFFIX.int_sort import (
    measure_insertion_memory,
    bubble,
    measure_bubble_cpu,
)
from basic_sort_UNIQUE_SUFFIX.int_sort import quick, measure_quick_cpu


def is_sorted(int_list):
    """
    Testing oracle: True if list is sorted nondecreasing.
    """
    return all(int_list[i] <= int_list[i + 1] for i in range(len(int_list) - 1))


@pytest.fixture
def int_lists():
    """
    Fixture creating test data for all sorting algorithms.

    We convert numpy arrays to regular Python lists so our
    sorting functions always receive lists and always return lists.
    """
    return [
        [3, 2, 1],  # reverse sorted
        [1, 1, 1],  # duplicates
        list(np.random.randint(low=-10, high=200, size=5)),  # random ints
        [],  # empty
        [2],  # single element
        [5, -1, 5, 2, 0],  # mixed negatives/duplicates
    ]

    # Bubble sort tests


def test_bubble_sorts_correctly(int_lists):
    """
    Test that bubble sort produces correctly sorted output.
    """
    for lst in int_lists:
        out = bubble(lst)
        assert out == sorted(lst), f"Bubble sort failed on {lst}"


def test_bubble_does_not_change_input(int_lists):
    """
    Test that bubble sort does not modify the input list.
    """
    for lst in int_lists:
        original = lst.copy()
        _ = bubble(lst)
        assert lst == original, "Bubble sort should not change the input list"


def test_bubble_output_is_sorted(int_lists):
    """
    Test that bubble sort output is sorted.
    """
    for lst in int_lists:
        out = bubble(lst)
        assert is_sorted(out), f"Bubble output not sorted: {out}"


def test_bubble_cpu_measurement():
    """
    Test the CPU measurement function for bubble sort.
    """
    data = [5, 3, 1]
    result = measure_bubble_cpu(data, runs=3)

    assert isinstance(result, dict)
    assert "sorted" in result
    assert "avg_cpu_time" in result
    assert "avg_rss_bytes" in result
    assert result["sorted"] == sorted(data)
    assert isinstance(result["avg_cpu_time"], float)
    assert isinstance(result["avg_rss_bytes"], (int, float))


# Quick sort tests


def test_quick_sorts_correctly(int_lists):
    """
    Test that quick sort produces correctly sorted output.
    """
    for lst in int_lists:
        out = quick(lst)
        assert out == sorted(lst), f"Quick sort failed on {lst}"


def test_quick_does_not_change_input(int_lists):
    """
    Quick sort should NOT mutate the original input list.
    """
    for lst in int_lists:
        original = lst.copy()
        _ = quick(lst)
        assert lst == original, "Quick sort modified the input list"


def test_quick_output_is_sorted(int_lists):
    """
    Output must be sorted nondecreasing.
    """
    for lst in int_lists:
        out = quick(lst)
        assert is_sorted(out), f"Quick output not sorted: {out}"


def test_quick_cpu_measurement():
    """
    Test the CPU + memory measurement helper for quick sort.
    """
    data = [5, 3, 1, 4]
    result = measure_quick_cpu(data, runs=3)

    assert isinstance(result, dict), "measure_quick_cpu should return a dict"
    assert "sorted" in result, "Missing 'sorted' key"
    assert "avg_cpu_time" in result, "Missing 'avg_cpu_time' key"
    assert "avg_rss_bytes" in result, "Missing 'avg_rss_bytes' key"

    assert result["sorted"] == sorted(
        data
    ), "Quick sort measurement returned incorrect output"
    assert isinstance(result["avg_cpu_time"], float), "avg_cpu_time should be a float"
    assert isinstance(
        result["avg_rss_bytes"], (int, float)
    ), "avg_rss_bytes should be numeric"


# Insertion sort tests


def test_insertion_sorts_correctly(int_lists):
    for lst in int_lists:
        out = insertion(lst)
        assert out == sorted(lst), f"Insertion sort failed on {lst}"


def test_insertion_does_not_change_input(int_lists):
    for lst in int_lists:
        original = lst.copy()
        _ = insertion(lst)
        assert lst == original, "Insertion sort should not change the input list"


def test_insertion_output_is_sorted(int_lists):
    for lst in int_lists:
        out = insertion(lst)
        assert is_sorted(out), f"Insertion output not sorted: {out}"


def test_insertion_memory():
    data = [5, 3, 1]
    result = measure_insertion_memory(data, runs=3)

    assert isinstance(result, dict)
    assert "sorted" in result
    assert "avg_rss_bytes" in result
    assert result["sorted"] == sorted(data)
    assert isinstance(result["avg_rss_bytes"], (int, float))


# Overall test report


def test_measurements_report():
    """
    Print resource-usage measurements for README table.

    This is NOT a strict performance test (values can vary by OS/runner),
    so we only assert the functions return the expected structure.
    """
    rng = np.random.default_rng(seed=1337)
    data = list(rng.integers(low=-10, high=200, size=5000))

    bubble_stats = measure_bubble_cpu(data, runs=5)
    quick_stats = measure_quick_cpu(data, runs=5)
    insertion_stats = measure_insertion_memory(data, runs=5)

    # structural asserts
    assert "avg_cpu_time" in bubble_stats
    assert "avg_rss_bytes" in bubble_stats

    assert "avg_cpu_time" in quick_stats
    assert "avg_rss_bytes" in quick_stats

    assert "avg_rss_bytes" in insertion_stats
    assert "after_rss_bytes" in insertion_stats

    # print results for CI logs
    print(
        f"[MEASURE] bubble avg_cpu_time={bubble_stats['avg_cpu_time']:.6f}s "
        f"avg_rss_bytes={bubble_stats['avg_rss_bytes']:.0f}"
    )
    print(
        f"[MEASURE] quick avg_cpu_time={quick_stats['avg_cpu_time']:.6f}s "
        f"avg_rss_bytes={quick_stats['avg_rss_bytes']:.0f}"
    )
    print(
        f"[MEASURE] insertion avg_rss_bytes={insertion_stats['avg_rss_bytes']:.0f} "
        f"after_rss_bytes={insertion_stats['after_rss_bytes']:.0f}"
    )
