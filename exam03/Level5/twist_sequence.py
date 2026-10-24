def twist_sequence(arr: list[int], k: int) -> list[int]:
    if len(arr) == 0:
        return []

    n = len(arr)

    k = k % n

    last_part = arr[n - k:]   # elements from index n-k to the end
    first_part = arr[:n - k]  # elements from the start up to index n-k

    return last_part + first_part


print(twist_sequence([1, 2, 3, 4, 5], 2))  # [4, 5, 1, 2, 3]
print(twist_sequence([1, 2, 3, 4, 5], 0))  # [1, 2, 3, 4, 5]
print(twist_sequence([1, 2, 3, 4, 5], 7))  # [4, 5, 1, 2, 3]
print(twist_sequence([], 3))               # []
