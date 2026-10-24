def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    result = []
    i = 0   # position in list1
    j = 0   # position in list2

    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    while i < len(list1):
        result.append(list1[i])
        i += 1

    while j < len(list2):
        result.append(list2[j])
        j += 1

    return result


print(shadow_merge([1, 3, 5], [2, 4, 6]))
