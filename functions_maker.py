import sympy as sp

def create_u_symbol(i, j, matrix):
    if matrix[i][j] != '?':
        return matrix[i][j]
    else:
        return sp.Symbol('U({},{})'.format(i, j))

def create_v_symbol(i, j, matrix):
    if matrix[i][j] != '?':
        return matrix[i][j]
    else:
        return sp.Symbol('V({},{})'.format(i, j))

def save_unknowns_u(f, unknowns_u):
    for symbol in f.free_symbols:
        if symbol not in unknowns_u:
            unknowns_u.append(symbol)

def save_unknowns_v(f, unknowns_v):
    for symbol in f.free_symbols:
        if symbol not in unknowns_v:
            unknowns_v.append(symbol)

# Generates and save functions for matrix U
def create_functions_u(matrix_u):
    functions_u = []
    unknowns_u = []
    for i in range(1, len(matrix_u)-1):
        for j in range(1, len(matrix_u[i])-1):
            if matrix_u[i][j] != 0:
                U_ij = create_u_symbol(i, j, matrix_u)
                U_i_plus_1_j = create_u_symbol(i + 1, j, matrix_u)
                U_i_minus_1_j = create_u_symbol(i - 1, j, matrix_u)
                U_i_j_plus_1 = create_u_symbol(i, j + 1, matrix_u)
                U_i_j_minus_1 = create_u_symbol(i, j - 1, matrix_u)
                V_ij = create_v_symbol(i, j, matrix_u)
                f = U_i_plus_1_j + U_i_minus_1_j + U_i_j_plus_1 + U_i_j_minus_1 - 4 * U_ij - 1/2 * U_ij * \
                    U_i_plus_1_j + 1/2 * U_ij * U_i_minus_1_j - 1/2 * \
                    V_ij * U_i_j_plus_1 + 1/2 * V_ij * U_i_j_minus_1
                functions_u.append(f)
                save_unknowns_u(f, unknowns_u)
    return functions_u, unknowns_u

# Generates and save functions for matrix V
def create_functions_v(matrix_v):
    functions_v = []
    unknowns_v = []
    for i in range(1, len(matrix_v)-1):
        for j in range(1, len(matrix_v[i])-1):
            if matrix_v[i][j] != 0:
                V_ij = create_v_symbol(i, j, matrix_v)
                V_i_plus_1_j = create_v_symbol(i + 1, j, matrix_v)
                V_i_minus_1_j = create_v_symbol(i - 1, j, matrix_v)
                V_i_j_plus_1 = create_v_symbol(i, j + 1, matrix_v)
                V_i_j_minus_1 = create_v_symbol(i, j - 1, matrix_v)
                U_ij = create_u_symbol(i, j, matrix_v)
                f = V_i_plus_1_j + V_i_minus_1_j + V_i_j_plus_1 + V_i_j_minus_1 - 4 * V_ij - 1/2 * U_ij * \
                    V_i_plus_1_j + 1/2 * U_ij * V_i_minus_1_j - 1/2 * \
                    V_ij * V_i_j_plus_1 + 1/2 * V_ij * V_i_j_minus_1
                functions_v.append(f)
                save_unknowns_v(f, unknowns_v)
    return functions_v, unknowns_v

# Order functions replacing U(i,j) or V(i,j) for Ui or Vi structure in symbol for derivate in U or V
def __order_functions(unknown, unknowns, functions):
    new_unknowns = []
    index = 1
    for i, symbol in enumerate(unknowns):
        if unknown in str(symbol):
            inc = sp.Symbol(f'{unknown}{(index)}')
            for j, function in enumerate(functions):
                functions[j] = function.subs(symbol, inc)
            new_unknowns.append(inc)
            index=index+1
    return new_unknowns

# Create definitive functions for U and V
def create_functions(matrix_u, matrix_v):
    df_unknowns_u = []
    df_unknowns_v = []

    functions_u, unknowns_u = create_functions_u(matrix_u)
    functions_v, unknowns_v = create_functions_v(matrix_v)

    # Order functions replacing U(i,j) for Ui structure in symbol for derivate in U functions
    df_unknowns_u = __order_functions('U', unknowns_u, functions_u)
    df_unknowns_u = df_unknowns_u + __order_functions('V', unknowns_u, functions_u)
    df_unknowns_v = __order_functions('U', unknowns_v, functions_v)
    df_unknowns_v = df_unknowns_v + __order_functions('V', unknowns_v, functions_v)

    return functions_u, df_unknowns_u, functions_v, df_unknowns_v

# Generate jacobian functions deriving respecting unknowns for U or V
def create_jacobian(unknown, unknowns, functions):
    size = len(functions)
    jacobian = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            var = f'{unknown}{(j+1)}'
            if var in str(functions[i]):
                dif = sp.diff(functions[i], sp.Symbol(var))
                jacobian[i][j] = sp.lambdify(unknowns, dif)
    return jacobian

# Become functions to lambda expressions for U or V
def functions_to_lambda(functions, unknowns):
    for i in range(len(functions)):
        functions[i] = sp.lambdify(unknowns, functions[i])