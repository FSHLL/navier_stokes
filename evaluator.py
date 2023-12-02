import numpy as np

# Evaluate jacobian functions for definitive values
def evaluate_jacobian(jacobian, x):
    new_jacobian = [row.copy() for row in jacobian]
    for i in range(len(jacobian)):
        for j in range(len(jacobian[i])):
            if jacobian[i][j] != 0:
                new_jacobian[i][j] = jacobian[i][j](*x)
    return np.array(new_jacobian)

# Evaluate functions for definitive values
def evaluate_functions(functions, x, negative=False):
    functions_result = []
    for function in functions:
        result = function(*x)
        if negative :
            result = result*-1
        functions_result.append(result)
    return np.array(functions_result)

def conjugate_gradient(m_a, v_b, v_x, tol=1e-6, k_max=1000):
    x = v_x
    r = v_b - np.dot(m_a, v_x)
    p = r
    p_i = np.dot(r, p)
    p_0 = p_i
    k = 0
    while k < k_max:
        if p_i < tol * p_0:
            break
        a_p = np.dot(m_a, p)
        m = np.dot(p, a_p)
        alpha = p_i / m

        x = x + alpha*p
        r = r - alpha*a_p

        p_old = p_i
        p_i = np.dot(r, r)

        gamma = p_i/p_old

        p = r + gamma*p

        k=k+1

    return np.array(x)
