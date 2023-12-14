import sympy as sp
import numpy as np

def __create_polynomials(matrix, symbol):
    p = len(matrix)-1
    f = 1
    polynomials = []
    for i in range(1, p):
        for j in range(1, p):
            if i != j:
                f = f * (symbol - j)/(i - j)
        polynomials.append(f)
        f = 1
    return polynomials

def create_df_polynomial(matrix):
    x = np.arange(9)
    y = np.arange(9)

    x_s = sp.Symbol('x')
    y_s = sp.Symbol('y')

    u_s = create_polynomials(x, x_s)
    v_s = create_polynomials(y, y_s)
    df = 0

    for i, u in enumerate(u_s, 1):
        f = 0
        for j, v in enumerate(v_s, 1):
            f = f + matrix[i][j]*v
        df = df + u*(f)

    return sp.lambdify((x_s, y_s), df)

def add_rows_and_columns_interleaved(matrix):
    rows, columns = len(matrix), len(matrix[0])

    new_matrix = [['?'] * (2 * columns - 1) for _ in range(2 * rows - 1)]

    for i in range(rows):
        for j in range(columns):
            new_matrix[2 * i][2 * j] = matrix[i][j]

    rows, columns = len(new_matrix), len(new_matrix[0])

    for i in range(rows):
        new_matrix[i][0] = 1

    for i in range(columns):
        new_matrix[0][i] = 0

    for i in range(columns):
        new_matrix[columns-1][i] = 0

    for i in range(rows):
        new_matrix[i][rows-1] = 0

    return new_matrix

def add_columns_interleaved(matrix):
    rows, columns = len(matrix), len(matrix[0])

    new_columns = 2 * columns - 1
    new_matrix = [[0] * new_columns for _ in range(rows)]

    for i in range(rows):
        for j in range(columns):
            new_matrix[i][2 * j] = matrix[i][j]

            if j < columns - 1:
                new_matrix[i][2 * j + 1] = "?"

    rows, columns = len(new_matrix), len(new_matrix[0])

    for i in range(rows):
        new_matrix[i][0] = 1

    for i in range(columns):
        new_matrix[0][i] = 0
        new_matrix[rows-1][i] = 0

    return new_matrix

def apply_interpolation(matrix, p):
    new_matrix = add_columns_interleaved(matrix)
    rows, columns = len(new_matrix)-1, len(new_matrix[0])-1

    for i in range(1,rows):
        if new_matrix[i][1] == '?':
            for j in range(1, columns):
                if new_matrix[i][j] == '?':
                    new_matrix[i][j] = p(i, j)

    return new_matrix

def apply_interpolation_2(matrix, p, n=25):
    new_x = np.linspace(1, len(matrix)-2, n-2)
    new_y = np.linspace(1, len(matrix[0])-2, n-2)

    new_matrix = np.zeros((n, n))

    for i, x in enumerate(new_x, 1):
        for j, y in enumerate(new_y, 1):
            new_matrix[i, j] = p(x, y)

    rows, columns = len(new_matrix), len(new_matrix[0])

    for i in range(rows):
        new_matrix[i][0] = 1

    for i in range(columns):
        new_matrix[0][i] = 0
        new_matrix[rows-1][i] = 0

    return new_matrix
