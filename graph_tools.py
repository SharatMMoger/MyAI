import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

x = symbols('x')

def plot_function(expression):

    expr = sympify(expression)

    func = lambdify(x, expr, "numpy")

    x_values = np.linspace(-10, 10, 400)

    y_values = func(x_values)

    plt.figure(figsize=(8,5))
    plt.plot(x_values, y_values)

    plt.grid(True)

    plt.title(expression)

    plt.xlabel("x")
    plt.ylabel("y")

    plt.show()