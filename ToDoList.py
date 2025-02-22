import tkinter as tk
from tkinter import messagebox

def add_task():
    task = task_entry.get()
    if task:
        task_frame = tk.Frame(tasks_frame)
        task_var = tk.IntVar()
        
        def toggle_strikethrough():
            if task_var.get() == 1:
                task_label.config(font=("TkDefaultFont", 10, "overstrike"))
            else:
                task_label.config(font=("TkDefaultFont", 10, "normal"))

        task_checkbox = tk.Checkbutton(task_frame, variable=task_var, command=toggle_strikethrough)
        task_checkbox.pack(side=tk.LEFT)
        task_label = tk.Label(task_frame, text=task)
        task_label.pack(side=tk.LEFT)
        task_frame.pack(anchor="w")
        task_entry.delete(0, tk.END)
        tasks.append((task_frame, task_var, task_label))
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    unchecked_tasks = []
    for task_frame, task_var, _ in tasks:
        if task_var.get() == 1:
            task_frame.destroy()
        else:
            unchecked_tasks.append((task_frame, task_var, _))
    tasks.clear()
    tasks.extend(unchecked_tasks)

def clear_tasks():
    for task_frame, _, _ in tasks:
        task_frame.destroy()
    tasks.clear()

window = tk.Tk()
window.title("To-Do List")

tasks = []

frame = tk.Frame(window)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=30)
task_entry.pack(side=tk.LEFT, padx=10)

tk.Button(frame, text="Add Task", command=add_task).pack(side=tk.LEFT)

tasks_frame = tk.Frame(window)
tasks_frame.pack(pady=10)

action_frame = tk.Frame(window)
action_frame.pack(pady=10)

tk.Button(action_frame, text="Delete Selected Task", command=delete_task).pack(side=tk.LEFT, padx=10)
tk.Button(action_frame, text="Clear Tasks", command=clear_tasks).pack(side=tk.LEFT, padx=10)

window.mainloop()
