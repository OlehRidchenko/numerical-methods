import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ------------------ ФУНКЦІЯ З ЛАБИ №3 ------------------
# y = a * e^(b*x)
# Ти можеш змінити під свої коефіцієнти!
a = 0.0021
b = 0.135


def f(x):
    return a * np.exp(b * x)


# ------------------ Лагранж ------------------
def lagrange_interpolation(x, y, xp):
    yp = 0
    n = len(x)
    for i in range(n):
        L = 1
        for j in range(n):
            if i != j:
                L *= (xp - x[j]) / (x[i] - x[j])
        yp += L * y[i]
    return yp


# ------------------ Побудова ------------------
def build():
    try:
        xmin = float(entry_min.get())
        xmax = float(entry_max.get())
    except:
        return

    h = (xmax - xmin) / 10
    x_nodes = np.array([xmin + i * h for i in range(11)])
    y_nodes = f(x_nodes)

    # Очистити таблицю
    for row in table.get_children():
        table.delete(row)

    for xi, yi in zip(x_nodes, y_nodes):
        table.insert("", tk.END, values=(round(xi, 4), round(yi, 6)))

    # Графік
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    # малюємо точки
    ax.scatter(x_nodes, y_nodes, color="red", label="Вузли інтерполяції")

    # малюємо поліном
    x_plot = np.linspace(xmin, xmax, 400)
    y_plot = [lagrange_interpolation(x_nodes, y_nodes, xx) for xx in x_plot]
    ax.plot(x_plot, y_plot, label="Поліном Лагранжа")

    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Інтерполяція поліномом Лагранжа")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Лабораторна №4 — Інтерполяція Лагранжа")
root.geometry("950x600")

settings = ttk.LabelFrame(root, text="Ввід даних")
settings.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

ttk.Label(settings, text="xmin").pack(side=tk.LEFT, padx=5)
entry_min = ttk.Entry(settings, width=10)
entry_min.pack(side=tk.LEFT, padx=5)
entry_min.insert(0, "46")

ttk.Label(settings, text="xmax").pack(side=tk.LEFT, padx=5)
entry_max = ttk.Entry(settings, width=10)
entry_max.pack(side=tk.LEFT, padx=5)
entry_max.insert(0, "60")

ttk.Button(settings, text="Розрахувати", command=build).pack(side=tk.LEFT, padx=10)

# Таблиця
table_frame = ttk.LabelFrame(root, text="Таблиця вузлів")
table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

table = ttk.Treeview(table_frame, columns=("x", "y"), show="headings", height=20)
table.heading("x", text="x")
table.heading("y", text="y")
table.column("x", width=80)
table.column("y", width=150)
table.pack()

# Графік
plot_frame = ttk.LabelFrame(root, text="Графік")
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
