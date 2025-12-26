import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# -------- Інтегральна функція --------
def f(x):
    return 1 / (math.sqrt(x) + 2)


# --------- Методи чисельного інтегрування ---------

def rectangle_method(a, b, n):
    h = (b - a) / n
    s = 0
    for i in range(n):
        x = a + i * h + h / 2
        s += f(x)
    return s * h


def trapezoid_method(a, b, n):
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def monte_carlo_method(a, b, n):
    s = 0
    for i in range(n):
        x = random.uniform(a, b)
        s += f(x)
    return (b - a) * s / n


# -------- GUI логіка --------
def calculate():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())

        N_values = [10, 20, 50, 100, 1000]

        for item in table.get_children():
            table.delete(item)

        rect_results = []
        trap_results = []
        mc_results = []

        for N in N_values:
            rect = rectangle_method(a, b, N)
            trap = trapezoid_method(a, b, N)
            mc = monte_carlo_method(a, b, N)

            rect_results.append(rect)
            trap_results.append(trap)
            mc_results.append(mc)

            table.insert("", "end",
                         values=(N,
                                 f"{rect:.8f}",
                                 f"{trap:.8f}",
                                 f"{mc:.8f}"))

        ax.clear()
        ax.plot(N_values, rect_results, marker="o", label="Метод прямокутників")
        ax.plot(N_values, trap_results, marker="o", label="Метод трапецій")
        ax.plot(N_values, mc_results, marker="o", label="Метод Монте-Карло")

        ax.set_xscale("log")
        ax.set_xlabel("N (логарифмічна шкала)")
        ax.set_ylabel("Значення інтеграла")
        ax.set_title("Зближення результатів до істинного значення")
        ax.grid(True)
        ax.legend()

        canvas.draw()

    except:
        pass


# ----------- GUI -----------
root = tk.Tk()
root.title("Чисельне обчислення визначеного інтеграла")
root.geometry("950x650")
root.configure(bg="#eef2f5")

frame_top = tk.LabelFrame(root, text="Вхідні дані", bg="#eef2f5", font=("Arial", 11, "bold"))
frame_top.pack(fill="x", padx=10, pady=10)

tk.Label(frame_top, text="a =", bg="#eef2f5").grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(frame_top, width=10)
entry_a.grid(row=0, column=1, padx=5)
entry_a.insert(0, "0.5")

tk.Label(frame_top, text="b =", bg="#eef2f5").grid(row=0, column=2, padx=5)
entry_b = tk.Entry(frame_top, width=10)
entry_b.grid(row=0, column=3, padx=5)
entry_b.insert(0, "1.3")

btn = tk.Button(frame_top, text="Обчислити", font=("Arial", 10, "bold"),
                bg="#4CAF50", fg="white", command=calculate)
btn.grid(row=0, column=4, padx=20)

frame_table = tk.LabelFrame(root, text="Результати", bg="#eef2f5", font=("Arial", 11, "bold"))
frame_table.pack(fill="x", padx=10, pady=5)

columns = ("N", "Прямокутники", "Трапеції", "Монте-Карло")
table = ttk.Treeview(frame_table, columns=columns, show="headings", height=6)

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=200)

table.pack(fill="x", padx=10, pady=5)

frame_graph = tk.LabelFrame(root, text="Графічна інтерпретація", bg="#eef2f5", font=("Arial", 11, "bold"))
frame_graph.pack(fill="both", expand=True, padx=10, pady=10)

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()
