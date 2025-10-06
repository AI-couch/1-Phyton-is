import tkinter as tk           # цех №1
from tkinter import ttk        # цех №2

root = tk.Tk()
root.title("Завод виджетов")

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack(padx=10, pady=10)

# Два «робота»-фигуры на одном конвейере
bot_wheels = canvas.create_rectangle(20, 80, 80, 140, fill="gold")   # колёса
bot_arms   = canvas.create_oval(200, 60, 260, 120, fill="skyblue")   # руки

step = 10
def move_right():
    # одна и та же «команда» (метод canvas.move) для разных роботов
    canvas.move(bot_wheels, step, 0)
    canvas.move(bot_arms, step, 0)

def paint_blue():
    # настройка «свойства» для одного из роботов
    canvas.itemconfigure(bot_wheels, fill="blue")

controls = ttk.Frame(root)     # тип из другого модуля (ttk)
controls.pack(pady=5)

ttk.Button(controls, text="Вперёд →", command=move_right).pack(side="left", padx=5)
ttk.Button(controls, text="Покрасить", command=paint_blue).pack(side="left", padx=5)

ttk.Progressbar(root, mode="indeterminate").pack(fill="x", padx=10, pady=5)
root.mainloop()
