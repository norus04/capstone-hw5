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
from basic_sort_UNIQUE_SUFFIX.int_sort import measure_insertion_memory


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


def test_bubble(int_lists):
    assert True


def test_quick(int_lists):
    assert True


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
