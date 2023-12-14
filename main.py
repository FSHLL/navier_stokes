import numpy as np
import matplotlib.pyplot as plt
import matrix_maker
import functions_maker
import newton_raphson
import interpolation

matrix_u, matrix_v = matrix_maker.create_matrix(9, 9)

functions_u, unknowns_u, functions_v, unknowns_v = functions_maker.create_functions(matrix_u, matrix_v)

jacobian_u = functions_maker.create_jacobian('U', unknowns_u, functions_u)
jacobian_v = functions_maker.create_jacobian('V', unknowns_v, functions_v)

# Become functions to lambda expressions for U
functions_maker.functions_to_lambda(functions_u, unknowns_u)

# Become functions to lambda expressions for V
functions_maker.functions_to_lambda(functions_v, unknowns_v)

X0 = np.ones_like(functions_u)
Y0 = np.ones_like(functions_v)

# Newton_raphson method with conjugate inverse
X0, Y0 = newton_raphson.eval_with_inv(X0, Y0, functions_u, jacobian_u, functions_v, jacobian_v)

# Newton_raphson method with conjugate gradient
# X0, Y0 = newton_raphson.eval_with_alg(X0, Y0, functions_u, jacobian_u, functions_v, jacobian_v, k_max=0)

index = 0
for i in range(1, len(matrix_u)-1):
    for j in range(1, len(matrix_u[i])-1):
        if matrix_u[i][j] != 0:
            matrix_u[i][j] = X0[index]
            index = index+1

p = interpolation.create_df_polynomial(matrix_u)

print(p(1, 3))
matrix_u = interpolation.apply_interpolation_2(matrix_u, p, 10)

plt.imshow(matrix_u)
plt.title( "2-D Heat Map" )
plt.colorbar()
plt.show()