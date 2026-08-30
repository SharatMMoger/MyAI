from sympy import (
    symbols,
    sympify,
    solve,
    factor,
    diff,
    integrate,
    simplify,
    expand,
    limit,
    Matrix,
    Poly,
    Eq
)

x = symbols('x')

# -------------------
# Algebra
# -------------------

def solve_equation(expression):
    return solve(sympify(expression), x)

def factor_expression(expression):
    return factor(sympify(expression))

def differentiate(expression):
    return diff(sympify(expression), x)

def integrate_expression(expression):
    return integrate(sympify(expression), x)

def simplify_expression(expression):
    return simplify(sympify(expression))

def expand_expression(expression):
    return expand(sympify(expression))

def limit_expression(expression):
    return limit(sympify(expression), x, 0)

def polynomial_roots(expression):
    return solve(sympify(expression), x)

def polynomial_degree(expression):
    return Poly(sympify(expression), x).degree()

# -------------------
# Linear Equations
# -------------------

def solve_linear_system(a1, b1, c1, a2, b2, c2):
    x, y = symbols('x y')

    eq1 = Eq(a1 * x + b1 * y, c1)
    eq2 = Eq(a2 * x + b2 * y, c2)

    return solve((eq1, eq2), (x, y))

# -------------------
# Matrices
# -------------------

def matrix_determinant(matrix_data):
    m = Matrix(matrix_data)
    return m.det()

def matrix_inverse(matrix_data):
    m = Matrix(matrix_data)
    return m.inv()

def matrix_transpose(matrix_data):
    m = Matrix(matrix_data)
    return m.T

def matrix_add(matrix1, matrix2):
    m1 = Matrix(matrix1)
    m2 = Matrix(matrix2)
    return m1 + m2

def matrix_multiply(matrix1, matrix2):
    m1 = Matrix(matrix1)
    m2 = Matrix(matrix2)
    return m1 * m2

def matrix_rank(matrix_data):
    m = Matrix(matrix_data)
    return m.rank()

def matrix_eigenvalues(matrix_data):
    m = Matrix(matrix_data)
    return m.eigenvals()