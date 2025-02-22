import customtkinter as ctk
import time
import math
from tkinter import messagebox

# Initialize main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Timer & To-Do List")
root.geometry("1000x600")  # Adjusted size

tasks = []

# ------------------------ TIMER FUNCTIONS ------------------------

hour = ctk.StringVar(value="00")
minute = ctk.StringVar(value="05")
second = ctk.StringVar(value="00")

def relax():
    """Reset timer to relaxation mode (5 mins)."""
    hour.set("00")
    minute.set("05")
    second.set("00")

def countdown():
    """Start the countdown timer."""
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
        total_time = temp

        if temp < 0:
            messagebox.showerror("Error", "Invalid time input!")
            return
        
        start_button.configure(state="disabled")
        canvas.delete("progress")

        def update_timer():
            nonlocal temp
            if temp >= 0:
                mins, secs = divmod(temp, 60)
                hours, mins = divmod(mins, 60)

                hour.set(f"{hours:02d}")
                minute.set(f"{mins:02d}")
                second.set(f"{secs:02d}")

                angle = 360 * (total_time - temp) / total_time
                
                start_angle = 90
                end_angle = start_angle - angle
                
                canvas.delete("progress")
                canvas.create_arc(padding, padding, circle_size + padding - 20, 
                                circle_size + padding - 20,
                                start=start_angle,
                                extent=-angle,
                                outline='blue',
                                width=5,
                                style="arc",
                                tags="progress")

                if temp > 0:
                    temp -= 1
                    root.after(1000, update_timer)
                else:
                    messagebox.showinfo("Time Countdown", "Time's up!")
                    start_button.configure(state="normal")

        update_timer()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        start_button.configure(state="normal")

# ------------------------ TO-DO LIST FUNCTIONS ------------------------

def toggle_strikethrough(task_label, task_var):
    """Strike through text when task is checked."""
    if task_var.get() == 1:
        task_label.configure(font=("Arial", 16, "overstrike"), text_color="white")
    else:
        task_label.configure(font=("Arial", 16, "normal"), text_color="white")

def add_task():
    """Add a new task to the list."""
    task = task_entry.get()
    if task:
        task_frame = ctk.CTkFrame(tasks_frame, fg_color="transparent")
        task_var = ctk.IntVar()

        task_label = ctk.CTkLabel(task_frame, text=task, font=("Arial", 16), text_color="white")
        task_checkbox = ctk.CTkCheckBox(task_frame, text="", variable=task_var, 
                                        command=lambda: toggle_strikethrough(task_label, task_var))

        task_checkbox.pack(side="left", padx=5, pady=3)
        task_label.pack(side="left", padx=10, pady=3)
        task_frame.pack(anchor="w", pady=5, fill="x")

        task_entry.delete(0, "end")
        tasks.append((task_frame, task_var, task_label))
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    """Delete selected tasks."""
    unchecked_tasks = []
    for task_frame, task_var, task_label in tasks:
        if task_var.get() == 1:
            task_frame.destroy()
        else:
            unchecked_tasks.append((task_frame, task_var, task_label))
    tasks.clear()
    tasks.extend(unchecked_tasks)

def clear_tasks():
    """Clear all tasks."""
    for task_frame, _, _ in tasks:
        task_frame.destroy()
    tasks.clear()

# ------------------------ UI LAYOUT ------------------------

main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# -------- LEFT SIDE: TIMER --------
timer_frame = ctk.CTkFrame(main_frame)
timer_frame.pack(side="left", padx=20, fill="both", expand=True)

# Canvas setup for Timer
canvas_size = 250
canvas = ctk.CTkCanvas(master=timer_frame, width=canvas_size, height=canvas_size, 
                      bg=root.cget('bg'), highlightthickness=0)
canvas.pack(pady=10)

# Circle dimensions
padding = 25
circle_size = canvas_size - 2 * padding
canvas.create_oval(padding, padding, circle_size + padding, circle_size + padding, 
                  outline='gray', width=5)

# Timer labels (inside the circle)
center_x = canvas_size / 2
center_y = canvas_size / 2

hourLabel = ctk.CTkLabel(master=canvas, textvariable=hour, font=("Arial", 20))
hourLabel.place(x=center_x - 50, y=center_y, anchor="center")

colonLabel1 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", 20))
colonLabel1.place(x=center_x - 15, y=center_y, anchor="center")

minuteLabel = ctk.CTkLabel(master=canvas, textvariable=minute, font=("Arial", 20))
minuteLabel.place(x=center_x + 10, y=center_y, anchor="center")

colonLabel2 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", 20))
colonLabel2.place(x=center_x + 35, y=center_y, anchor="center")

secondLabel = ctk.CTkLabel(master=canvas, textvariable=second, font=("Arial", 20))
secondLabel.place(x=center_x + 65, y=center_y, anchor="center")

# Timer Buttons
start_button = ctk.CTkButton(timer_frame, text="Start Countdown", command=countdown, font=("Arial", 14, "bold"))
start_button.pack(pady=5)

relax_button = ctk.CTkButton(timer_frame, text="Relax (5 min)", command=relax, font=("Arial", 14, "bold"))
relax_button.pack(pady=5)

# -------- RIGHT SIDE: TO-DO LIST --------
todo_frame = ctk.CTkFrame(main_frame)
todo_frame.pack(side="right", padx=20, fill="both", expand=True)

tasks_frame = ctk.CTkFrame(todo_frame, fg_color="transparent")
tasks_frame.pack(fill="both", expand=True, pady=5)

buttons_frame = ctk.CTkFrame(todo_frame, fg_color="transparent")
buttons_frame.pack(fill="x", pady=5)

delete_button = ctk.CTkButton(buttons_frame, text="Delete Task", command=delete_task, 
                              fg_color="red", hover_color="darkred", font=("Arial", 14, "bold"))
delete_button.pack(side="left", padx=5, expand=True)

clear_button = ctk.CTkButton(buttons_frame, text="Clear Tasks", command=clear_tasks, 
                             fg_color="gray", hover_color="darkgray", font=("Arial", 14, "bold"))
clear_button.pack(side="left", padx=5, expand=True)

task_entry = ctk.CTkEntry(todo_frame, placeholder_text="Enter a task...", font=("Arial", 14))
task_entry.pack(pady=5, fill="x")

add_button = ctk.CTkButton(todo_frame, text="Add Task", command=add_task, font=("Arial", 14, "bold"))
add_button.pack(pady=5, fill="x")

# Run the main loop
root.mainloop()
