import customtkinter as ctk
import time
import math
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Timer & To-Do List")


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")


hour = ctk.StringVar(value="00")
minute = ctk.StringVar(value="03")
second = ctk.StringVar(value="00")
tasks = []
clear_flag = False  


def relax():
    hour.set("00")
    minute.set("05")
    second.set("00")

def countdown():
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
        total_time = temp

        if temp < 0:
            messagebox.showerror("Error", "Invalid time input!")
            return
        
        start_button.configure(state="disabled")
        canvas.delete("progress")
        relax_button.pack_forget()  

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
                
                
                arc_padding = padding  
                arc_size = circle_size  
                
                canvas.delete("progress")
                canvas.create_arc(
                    arc_padding, 
                    arc_padding, 
                    arc_padding + arc_size, 
                    arc_padding + arc_size,
                    start=start_angle,
                    extent=-angle,
                    outline='blue',
                    width=5,
                    style="arc",
                    tags="progress"
                )

                if temp > 0:
                    temp -= 1
                    root.after(1000, update_timer)
                else:
                    messagebox.showinfo("Time Countdown", "Time's up!")
                    start_button.configure(state="normal")
                    relax_button.pack(pady=5)  

        update_timer()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        start_button.configure(state="normal")



def toggle_strikethrough(task_label, task_var):
    if task_var.get() == 1:
        task_label.configure(font=("Arial", 18, "overstrike"), text_color="white")
    else:
        task_label.configure(font=("Arial", 18, "normal"), text_color="white")

def add_task():
    global clear_flag
    task = task_entry.get()
    if task:
        task_frame = ctk.CTkFrame(tasks_frame, fg_color="transparent")
        task_var = ctk.IntVar()

        task_label = ctk.CTkLabel(task_frame, text=task, font=("Arial", 18), text_color="white")
        task_checkbox = ctk.CTkCheckBox(task_frame, text="", variable=task_var, 
                                      command=lambda: toggle_strikethrough(task_label, task_var))

        task_checkbox.pack(side="left", padx=5, pady=3)
        task_label.pack(side="left", padx=10, pady=3)
        task_frame.pack(anchor="w", pady=5, fill="x")

        task_entry.delete(0, "end")
        tasks.append((task_frame, task_var, task_label))
        clear_flag = False  
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    global clear_flag
    unchecked_tasks = []
    for task_frame, task_var, task_label in tasks:
        if task_var.get() == 1:
            task_frame.destroy()
        else:
            unchecked_tasks.append((task_frame, task_var, task_label))
    tasks.clear()
    tasks.extend(unchecked_tasks)
    clear_flag = True  

def clear_tasks():
    global clear_flag
    for task_frame, _, _ in tasks:
        task_frame.destroy()
    tasks.clear()
    clear_flag = True  

def save_tasks():
    with open("tasks.txt", "w") as file:
        for task_frame, task_var, task_label in tasks:
            task = task_label.cget("text")
            file.write(task + "\n")
    messagebox.showinfo("Info", "Tasks saved successfully.")

def load_tasks():
    if clear_flag:
        messagebox.showwarning("Warning", "You cannot load tasks after clearing or deleting them.")
        return

    try:
        with open("tasks.txt", "r") as file:
            loaded_tasks = file.readlines()
            for task in loaded_tasks:
                task = task.strip()
                task_frame = ctk.CTkFrame(tasks_frame, fg_color="transparent")
                task_var = ctk.IntVar()

                task_label = ctk.CTkLabel(task_frame, text=task, font=("Arial", 18), text_color="white")
                task_checkbox = ctk.CTkCheckBox(task_frame, text="", variable=task_var, 
                                                command=lambda: toggle_strikethrough(task_label, task_var))

                task_checkbox.pack(side="left", padx=5, pady=3)
                task_label.pack(side="left", padx=10, pady=3)
                task_frame.pack(anchor="w", pady=5, fill="x")

                tasks.append((task_frame, task_var, task_label))
        messagebox.showinfo("Info", "Tasks loaded successfully.")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved tasks found.")



main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)


timer_frame = ctk.CTkFrame(main_frame)
timer_frame.pack(side="left", padx=20, fill="both", expand=True)


canvas_size = int(min(screen_width, screen_height) * 0.3)
canvas = ctk.CTkCanvas(master=timer_frame, width=canvas_size, height=canvas_size, 
                      bg=root.cget('bg'), highlightthickness=0)
canvas.pack(pady=10)


padding = 20
circle_size = canvas_size - 2 * padding
canvas.create_oval(padding, padding, circle_size + padding, circle_size + padding, 
                  outline='gray', width=5)


center_x = canvas_size / 2
center_y = canvas_size / 2
font_size = int(canvas_size * 0.09)

hourEntry = ctk.CTkEntry(master=canvas, textvariable=hour, font=("Arial", font_size), 
                        width=40, justify="center")
hourEntry.place(x=center_x - 60, y=center_y, anchor="center")

colonLabel1 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", font_size))
colonLabel1.place(x=center_x - 25, y=center_y, anchor="center")

minuteEntry = ctk.CTkEntry(master=canvas, textvariable=minute, font=("Arial", font_size), 
                          width=40, justify="center")
minuteEntry.place(x=center_x, y=center_y, anchor="center")

colonLabel2 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", font_size))
colonLabel2.place(x=center_x + 25, y=center_y, anchor="center")

secondEntry = ctk.CTkEntry(master=canvas, textvariable=second, font=("Arial", font_size), 
                          width=40, justify="center")
secondEntry.place(x=center_x + 60, y=center_y, anchor="center")


start_button = ctk.CTkButton(timer_frame, text="Start Countdown", command=countdown, font=("Arial", 14, "bold"))
start_button.pack(pady=5)

relax_button = ctk.CTkButton(timer_frame, text="Relax (5 min)", command=relax, font=("Arial", 14, "bold"))
relax_button.pack_forget()  


todo_frame = ctk.CTkFrame(main_frame)
todo_frame.pack(side="right", padx=20, fill="both", expand=True)

tasks_frame = ctk.CTkFrame(todo_frame, fg_color="transparent")
tasks_frame.pack(fill="both", expand=True, pady=5)

buttons_frame = ctk.CTkFrame(todo_frame, fg_color="transparent")
buttons_frame.pack(fill="x", pady=5)

delete_button = ctk.CTkButton(buttons_frame, text="Delete Selected Task", command=delete_task, fg_color="red", font=("Arial", 14, "bold"))
delete_button.pack(side="left", padx=5, expand=True)

clear_button = ctk.CTkButton(buttons_frame, text="Clear Tasks", command=clear_tasks, fg_color="gray", font=("Arial", 14, "bold"))
clear_button.pack(side="left", padx=5, expand=True)

save_button = ctk.CTkButton(buttons_frame, text="Save Tasks", command=save_tasks, font=("Arial", 14, "bold"))
save_button.pack(side="left", padx=5, expand=True)

load_button = ctk.CTkButton(buttons_frame, text="Load Tasks", command=load_tasks, font=("Arial", 14, "bold"))
load_button.pack(side="left", padx=5, expand=True)

task_entry = ctk.CTkEntry(todo_frame, font=("Arial", 18), placeholder_text="Enter new task...")
task_entry.pack(pady=10, padx=10, fill="x")

add_button = ctk.CTkButton(todo_frame, text="Add Task", command=add_task, font=("Arial", 14, "bold"))
add_button.pack(pady=5)

root.mainloop()