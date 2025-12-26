import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ----------------- Дані варіанту -----------------
x_data = np.array([46, 48, 50, 52, 54, 56, 58, 60], dtype=float)
y_data = np.array([500, 685, 925, 1100, 1325, 1520, 1780, 950], dtype=float)


# ----------------- Обчислення коефіцієнтів -----------------
def exponential_regression(x, y):
    ln_y = np.log(y)

    n = len(x)
    b = (n * np.sum(x * ln_y) - np.sum(x) * np.sum(ln_y)) / \
        (n * np.sum(x * x) - (np.sum(x)) ** 2)

    ln_a = (np.sum(ln_y) - b * np.sum(x)) / n
    a = np.exp(ln_a)

    return a, b


# ----------------- Побудова графіка -----------------
def build_regression():
    a, b = exponential_regression(x_data, y_data)

    # Очищення фрейму
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Точки експерименту
    ax.scatter(x_data, y_data, label="Експериментальні дані")

    # Побудова апроксимації
    x_reg = np.linspace(min(x_data), max(x_data), 200)
    y_reg = a * np.exp(b * x_reg)
    ax.plot(x_reg, y_reg, label=f"Регресія: y = {a:.3f}e^({b:.4f}x)")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Експоненційна регресія методом найменших квадратів")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# ----------------- ГОЛОВНЕ ВІКНО -----------------
root = tk.Tk()
root.title("Лабораторна №3 — Регресія")
root.geometry("900x600")

# ----------------- Таблиця -----------------
table_frame = ttk.LabelFrame(root, text="Експериментальні дані (x, y)")
table_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

table = ttk.Treeview(table_frame, columns=("x", "y"), show="headings", height=10)
table.heading("x", text="x")
table.heading("y", text="y")
table.column("x", width=80)
table.column("y", width=120)
table.pack()

for x, y in zip(x_data, y_data):
    table.insert("", tk.END, values=(x, y))

# ----------------- Кнопка -----------------
btn = ttk.Button(root, text="Побудувати регресію", command=build_regression)
btn.pack(pady=10)

# ----------------- Поле графіка -----------------
plot_frame = ttk.LabelFrame(root, text="Графік")
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
