import tkinter as tk
from tkinter import messagebox

# Function to add a task to the list
def add_task():
    task = task_entry.get()
    if task != "":
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task_text = tasks_listbox.get(selected_task_index)
        if not task_text.startswith("✓ "):
            tasks_listbox.delete(selected_task_index)
            tasks_listbox.insert(selected_task_index, "✓ " + task_text)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def clear_tasks():
    tasks_listbox.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("To-Do List")

frame = tk.Frame(window)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=30)
task_entry.pack(side=tk.LEFT, padx=10)

add_task_button = tk.Button(frame, text="Add Task", command=add_task)
add_task_button.pack(side=tk.LEFT)

tasks_listbox = tk.Listbox(window, width=50, height=10)
tasks_listbox.pack(pady=10)

action_frame = tk.Frame(window)
action_frame.pack(pady=10)

delete_task_button = tk.Button(action_frame, text="Delete Task", command=delete_task)
delete_task_button.pack(side=tk.LEFT, padx=10)

clear_tasks_button = tk.Button(action_frame, text="Clear Tasks", command=clear_tasks)
clear_tasks_button.pack(side=tk.LEFT, padx=10)

window.mainloop()
