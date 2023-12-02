import numpy as np
import evaluator

def eval_with_alg(X0, Y0, functions_u, jacobian_u, functions_v, jacobian_v, tol=1e-6, k_max=100, alg=None):
    k=0
    if alg == None:
        alg=evaluator.conjugate_gradient

    while np.linalg.norm(X0) > tol and np.linalg.norm(Y0) > tol and k <= k_max:
        values = np.concatenate((X0, Y0), axis=0)

        eval_jacobian_u = evaluator.evaluate_jacobian(jacobian_u, values)
        eval_functions_u = evaluator.evaluate_functions(functions_u, values, True)

        X0 = X0 + alg(eval_jacobian_u, eval_functions_u, np.zeros_like(eval_functions_u))

        eval_jacobian_v = evaluator.evaluate_jacobian(jacobian_v, values)
        eval_functions_v = evaluator.evaluate_functions(functions_v, values, True)

        Y0 = Y0 + alg(eval_jacobian_v, eval_functions_v, np.zeros_like(eval_functions_v))

        error_x = np.linalg.norm(X0)
        error_y = np.linalg.norm(Y0)

        print(f'Iteraction: {k}:')
        print(error_x)
        print(error_y)
        print('---------------------')
        k = k + 1
    return X0, Y0

def eval_with_inv(X0, Y0, functions_u, jacobian_u, functions_v, jacobian_v, tol=1e-6, k_max=100):
    k=0
    while np.linalg.norm(X0) > tol and np.linalg.norm(Y0) > tol and k <= k_max:
        values = np.concatenate((X0, Y0), axis=0)

        eval_jacobian_u = evaluator.evaluate_jacobian(jacobian_u, values)
        eval_functions_u = evaluator.evaluate_functions(functions_u, values)
        inv_jacobian_u = np.linalg.inv(eval_jacobian_u)

        X0 = X0 - np.dot(inv_jacobian_u, eval_functions_u)

        eval_jacobian_v = evaluator.evaluate_jacobian(jacobian_v, values)
        eval_functions_v = evaluator.evaluate_functions(functions_v, values)
        inv_jacobian_v = np.linalg.inv(eval_jacobian_v)

        Y0 = Y0 - np.dot(inv_jacobian_v, eval_functions_v)

        error_x = np.linalg.norm(X0)
        error_y = np.linalg.norm(Y0)

        print(f'Iteraction: {k}:')
        print(error_x)
        print(error_y)
        print('---------------------')
        k = k + 1
    return X0, Y0