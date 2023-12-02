
import math

def create_matrix(width, length):
    matrix_u = [[1 for _ in range(width)] for _ in range(length)]
    matrix_v = [[1 for _ in range(width)] for _ in range(length)]

    for i in range(length):
        for j in range(width):
            matrix_u[i][j] = '?'
            matrix_v[i][j] = '?'

    for i in range(length):
        matrix_u[i][0] = 1
        matrix_v[i][0] = 0

    for i in range(width):
        matrix_u[0][i] = 0
        matrix_v[0][i] = 0

    for i in range(width):
        matrix_u[length-1][i] = 0
        matrix_v[length-1][i] = 0

    for i in range(length):
        matrix_u[i][width-1] = 0
        matrix_v[i][width-1] = 0

    obstacle_1 = math.floor(width/2) - 1
    limit_obstacle_1 = math.floor(length/2)

    obstacle_2 = obstacle_1 + 1
    limit_obstacle_2 = limit_obstacle_1+1

    obstacle_3 = math.floor(length/2)
    limit_obstacle_3 = math.ceil(width/2)+1

    if width%2 == 0:
        limit_obstacle_3=limit_obstacle_3+1

    for i in range(1, limit_obstacle_1):
        matrix_u[i][obstacle_1] = 0
        matrix_v[i][obstacle_1] = 0

    for i in range(limit_obstacle_2, length -1):
        matrix_u[i][obstacle_2] = 0
        matrix_v[i][obstacle_2] = 0

    for i in range(limit_obstacle_3, width -1):
        matrix_u[obstacle_3][i] = 0
        matrix_v[obstacle_3][i] = 0

    return matrix_u, matrix_v