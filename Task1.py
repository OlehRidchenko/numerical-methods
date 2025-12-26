import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math


# --- Функція і її похідна ---
def f(x):
    return 3 * x - math.cos(x) - 1


def df(x):
    return 3 + math.sin(x)


# --- Методи ---
def bisection_method(a, b, eps):
    if f(a) * f(b) > 0:
        raise ValueError("На цьому проміжку немає кореня або їх парна кількість.")
    n = 0
    while (b - a) / 2 > eps:
        n += 1
        c = (a + b) / 2
        if f(c) == 0:
            return c, n
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2, n


def iteration_method(x0, eps, max_iter=1000):
    """Проста ітерація"""
    def phi(x):
        return (1 + math.cos(x)) / 3

    n = 0
    while n < max_iter:
        x1 = phi(x0)
        if abs(x1 - x0) < eps:
            return x1, n + 1
        x0 = x1
        n += 1
    return x1, n


def newton_method(x0, eps, max_iter=1000):
    """Метод Ньютона"""
    n = 0
    while n < max_iter:
        x1 = x0 - f(x0) / df(x0)
        if abs(x1 - x0) < eps:
            return x1, n + 1
        x0 = x1
        n += 1
    return x1, n


# --- Головне вікно ---
root = tk.Tk()
root.title("Пошук коренів рівняння 3x - cos(x) = 1")
root.geometry("950x650")
root.configure(bg="#f0f4f7")

# --- Введення даних ---
frame_input = tk.LabelFrame(root, text="Вхідні дані", bg="#f0f4f7", font=("Arial", 11, "bold"))
frame_input.pack(fill="x", padx=10, pady=5)

tk.Label(frame_input, text="a:", bg="#f0f4f7").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_a = tk.Entry(frame_input, width=10)
entry_a.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="b:", bg="#f0f4f7").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_b = tk.Entry(frame_input, width=10)
entry_b.grid(row=0, column=3, padx=5, pady=5)

# --- Вибір методу ---
frame_methods = tk.LabelFrame(root, text="Метод обчислення", bg="#f0f4f7", font=("Arial", 11, "bold"))
frame_methods.pack(fill="x", padx=10, pady=5)

method_var = tk.StringVar(value="bisection")

methods = [
    ("Метод ітерацій", "iteration"),
    ("Метод дихотомії (бісекції)", "bisection"),
    ("Метод Ньютона", "newton")
]

for i, (label, value) in enumerate(methods):
    tk.Radiobutton(frame_methods, text=label, variable=method_var, value=value, bg="#f0f4f7").grid(row=0, column=i, padx=15, pady=5)

# --- Кнопка ---
btn_calc = tk.Button(root, text="Обчислити", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_calc.pack(pady=5)


# --- Таблиця результатів ---
frame_table = tk.LabelFrame(root, text="Результати обчислень", bg="#f0f4f7", font=("Arial", 11, "bold"))
frame_table.pack(fill="x", padx=10, pady=5)

columns = ("ε (похибка)", "n (кількість ітерацій)", "x (корінь рівняння)", "f(x)")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=5)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

tree.pack(fill="x", padx=10, pady=5)

label_note = tk.Label(frame_table, text="f(x) — значення функції у знайденому корені (повинно бути ≈ 0)",
                      bg="#f0f4f7", fg="#333", font=("Arial", 9, "italic"))
label_note.pack(pady=(0, 5))

# --- Графік ---
frame_graph = tk.LabelFrame(root, text="Графік функції", bg="#f0f4f7", font=("Arial", 11, "bold"))
frame_graph.pack(fill="both", expand=True, padx=10, pady=5)

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)


# --- Функція обчислення ---
def calculate():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        eps_values = [0.01, 0.001, 0.0001]

        for item in tree.get_children():
            tree.delete(item)

        ax.clear()
        xs = np.linspace(a, b, 400)
        ys = [f(x) for x in xs]
        ax.plot(xs, ys, label="f(x) = 3x - cos(x) - 1", color="blue")
        ax.axhline(0, color="black", linewidth=1)

        colors = ["red", "green", "orange"]
        method = method_var.get()

        for i, eps in enumerate(eps_values):
            if method == "bisection":
                x, n = bisection_method(a, b, eps)
            elif method == "iteration":
                x, n = iteration_method((a + b) / 2, eps)
            else:
                x, n = newton_method((a + b) / 2, eps)

            fx = f(x)
            tree.insert("", "end", values=(eps, n, f"{x:.6f}", f"{fx:.2e}"))
            ax.plot(x, fx, "o", color=colors[i], label=f"ε={eps}, x≈{x:.5f}")

        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_title("Графік функції f(x)")
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Помилка", str(e))


btn_calc.config(command=calculate)

# --- Початкові значення ---
entry_a.insert(0, "0")
entry_b.insert(0, "1")

root.mainloop()
