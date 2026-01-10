# Sorting Algorithms for IntruWatch

from typing import List, Any, Callable


def insertion_sort(arr: List[Any], key: Callable = None) -> List[Any]:
    """Insertion Sort - O(n²) average, O(n) best case (nearly sorted)
    
    Good for:
    - Small datasets
    - Nearly sorted data
    - Online sorting (data arriving one at a time)
    """
    result = arr.copy()
    
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        
        if key:
            while j >= 0 and key(result[j]) > key(current):
                result[j + 1] = result[j]
                j -= 1
        else:
            while j >= 0 and result[j] > current:
                result[j + 1] = result[j]
                j -= 1
        
        result[j + 1] = current
    
    return result


def merge_sort(arr: List[Any], key: Callable = None) -> List[Any]:
    """Merge Sort - O(n log n) guaranteed
    
    Good for:
    - Large datasets
    - Stable sorting required
    - Linked lists
    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    
    return _merge(left, right, key)


def _merge(left: List[Any], right: List[Any], key: Callable = None) -> List[Any]:
    """Helper function to merge two sorted lists"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_val = key(left[i]) if key else left[i]
        right_val = key(right[j]) if key else right[j]
        
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: List[Any], key: Callable = None) -> List[Any]:
    """Quick Sort - O(n log n) average, O(n²) worst case
    
    Good for:
    - Large datasets
    - In-place sorting (memory efficient)
    - Random data
    """
    if len(arr) <= 1:
        return arr.copy()
    
    result = arr.copy()
    _quick_sort_helper(result, 0, len(result) - 1, key)
    return result


def _quick_sort_helper(arr: List[Any], low: int, high: int, key: Callable = None):
    """Helper function for quick sort"""
    if low < high:
        pivot_idx = _partition(arr, low, high, key)
        _quick_sort_helper(arr, low, pivot_idx - 1, key)
        _quick_sort_helper(arr, pivot_idx + 1, high, key)


def _partition(arr: List[Any], low: int, high: int, key: Callable = None) -> int:
    """Partition function for quick sort"""
    pivot = arr[high]
    pivot_val = key(pivot) if key else pivot
    i = low - 1
    
    for j in range(low, high):
        current_val = key(arr[j]) if key else arr[j]
        if current_val <= pivot_val:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def binary_search(sorted_arr: List[Any], target: Any, key: Callable = None) -> int:
    """Binary Search - O(log n)
    
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(sorted_arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = key(sorted_arr[mid]) if key else sorted_arr[mid]
        
        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def linear_search(arr: List[Any], target: Any, key: Callable = None) -> int:
    """Linear Search - O(n)
    
    Returns:
        Index of target if found, -1 otherwise
    """
    for i, item in enumerate(arr):
        val = key(item) if key else item
        if val == target:
            return i
    return -1


# Specialized sorting functions for IntruWatch

def sort_reg_numbers(reg_numbers: List[str]) -> List[str]:
    """Sort registration numbers using insertion sort"""
    return insertion_sort(reg_numbers)


def sort_by_priority(alerts: List[tuple]) -> List[tuple]:
    """Sort alerts by priority (first element)"""
    return merge_sort(alerts, key=lambda x: x[0])


def sort_guards_by_id(guards: List[tuple]) -> List[tuple]:
    """Sort guards by ID (second element)"""
    return quick_sort(guards, key=lambda x: x[1])


def search_user_by_reg(sorted_users: List[dict], reg_no: str) -> int:
    """Binary search for user by registration number"""
    return binary_search(
        sorted_users,
        reg_no,
        key=lambda x: x.get('Reg/Emp No', '')
    )
