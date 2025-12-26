import numpy as np
import matplotlib.pyplot as plt

# рівняння
def f(x, y):
    return np.exp(-x) - 2*y

# аналітичне рішення (y(0)=0)
def exact(x):
    return np.exp(-x) - np.exp(-2*x)

# ------------------ Метод Ейлера ------------------
def euler(x0, y0, h, xmax):
    xs = [x0]
    ys = [y0]
    while x0 < xmax:
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
        xs.append(x0)
        ys.append(y0)
    return np.array(xs), np.array(ys)

# ------------------ Рунге-Кутта 4 ------------------
def rk4(x0, y0, h, xmax):
    xs = [x0]
    ys = [y0]
    while x0 < xmax:
        k1 = f(x0, y0)
        k2 = f(x0 + h/2, y0 + h*k1/2)
        k3 = f(x0 + h/2, y0 + h*k2/2)
        k4 = f(x0 + h, y0 + h*k3)

        y0 = y0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        x0 = x0 + h

        xs.append(x0)
        ys.append(y0)

    return np.array(xs), np.array(ys)


# ---------------- ПАРАМЕТРИ ----------------
x0 = 0
y0 = 0
xmax = 2

# різні кроки
steps = [0.2, 0.1]

# графік
x_real = np.linspace(0, xmax, 400)
plt.plot(x_real, exact(x_real), 'k', label="Аналітичний розв'язок")

for h in steps:
    xe, ye = euler(x0, y0, h, xmax)
    plt.plot(xe, ye, '--', label=f"Ейлер h={h}")

    xr, yr = rk4(x0, y0, h, xmax)
    plt.plot(xr, yr, label=f"Рунге-Кутта h={h}")

plt.grid(True)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Розв'язування ОДР: Euler vs Runge–Kutta 4 vs Exact")
plt.legend()
plt.show()
