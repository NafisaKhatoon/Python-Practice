def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    result = []
    for row in matrix:
        result.append(row[::-1])
    return result


print(mirror_matrix([[3, 2, 1], [6, 5, 4]]))
