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

# Meditation variables
INHALE = "Breathe in..."
INHALE_HOLD = "Hold..."
EXHALE = "Breathe out..."
EXHALE_HOLD = "Hold..."
stop = False
center_x = 200
center_y = 200
radius = 10
max_radius = 100
min_radius = 10
frames_per_second = 40
frame_duration_milliseconds = 1000 // frames_per_second
box_stage_duration_seconds = 4
box_stage_duration_milliseconds = box_stage_duration_seconds * 1000
frames_per_box_stage = box_stage_duration_seconds * frames_per_second
radius_increment_size = (max_radius - min_radius) / (box_stage_duration_seconds * frames_per_second)

def relax():
    # Set the timer to 5 minutes
    hour.set("00")
    minute.set("05")
    second.set("00")

    # Hide the "Relax (5 min)" button
    relax_button.pack_forget()

    # Show the "Meditate" button underneath the "Relax (5 min)" button
    meditate_button.pack(pady=5)

def switch_to_meditation():
    # Hide the To-Do List frame
    todo_frame.pack_forget()

    # Show the Meditation frame
    meditation_frame.pack(side="right", padx=20, fill="both", expand=True)

def start_meditation():
    global stop
    stop = False
    render(1, INHALE, min_radius, radius_increment_size)

def terminate_meditation():
    global stop
    stop = True

def render(frame, stage_name, radius, radius_increment):
    if stop: return
    if frame % frames_per_box_stage == 0:
        if stage_name == INHALE:
            stage_name = INHALE_HOLD
            radius_increment = 0
        elif stage_name == INHALE_HOLD:
            stage_name = EXHALE
            radius_increment = -radius_increment_size
        elif stage_name == EXHALE:
            stage_name = EXHALE_HOLD
            radius_increment = 0
        elif stage_name == EXHALE_HOLD:
            stage_name = INHALE
            radius_increment = radius_increment_size
    message_label.configure(text=stage_name)
    meditation_canvas.coords(circle, center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    frame += 1
    radius += radius_increment
    root.after(frame_duration_milliseconds, render, frame, stage_name, radius, radius_increment)

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
        meditate_button.pack_forget()  # Hide the "Meditate" button when countdown starts

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
                    outline='#3B8EEA',
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
                    relax_button.pack(pady=5)  # Show the "Relax (5 min)" button again

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

        # Add an "Edit" button to the far right of the task frame
        edit_button = ctk.CTkButton(task_frame, text="Edit", width=50, font=("Arial", 12),
                                   command=lambda: edit_task(task_label))
        edit_button.pack(side="right", padx=5)

        task_checkbox.pack(side="left", padx=5, pady=3)
        task_label.pack(side="left", padx=10, pady=3)
        task_frame.pack(anchor="w", pady=5, fill="x")

        task_entry.delete(0, "end")
        tasks.append((task_frame, task_var, task_label))
        clear_flag = False  
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def edit_task(task_label):
    edit_window = ctk.CTkToplevel(root)
    edit_window.title("Edit Task")
    edit_window.geometry("300x100")

    # Ensure the edit window appears on top of the main window
    edit_window.lift()  # Bring the window to the top
    edit_window.focus_force()  # Force focus on the window
    edit_window.grab_set()  # Make the window modal

    new_task_entry = ctk.CTkEntry(edit_window, font=("Arial", 14))
    new_task_entry.pack(pady=10, padx=10, fill="x")
    new_task_entry.insert(0, task_label.cget("text"))

    def save_edited_task():
        new_task = new_task_entry.get()
        if new_task:
            task_label.configure(text=new_task)
            edit_window.grab_release()  # Release the grab before destroying the window
            edit_window.destroy()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    save_button = ctk.CTkButton(edit_window, text="Save", command=save_edited_task, font=("Arial", 14, "bold"))
    save_button.pack(pady=5)

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

                # Add an "Edit" button to the far right of the task frame
                edit_button = ctk.CTkButton(task_frame, text="Edit", width=50, font=("Arial", 12),
                                           command=lambda: edit_task(task_label))
                edit_button.pack(side="right", padx=5)

                task_checkbox.pack(side="left", padx=5, pady=3)
                task_label.pack(side="left", padx=10, pady=3)
                task_frame.pack(anchor="w", pady=5, fill="x")

                tasks.append((task_frame, task_var, task_label))
        messagebox.showinfo("Info", "Tasks loaded successfully.")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No saved tasks found.")

# Main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Timer frame
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
relax_button.pack(pady=5)

meditate_button = ctk.CTkButton(timer_frame, text="Meditate", command=switch_to_meditation, font=("Arial", 14, "bold"))
meditate_button.pack_forget()  # Initially hidden

# To-Do List frame
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

# Meditation frame
meditation_frame = ctk.CTkFrame(main_frame)
meditation_frame.pack_forget()  # Initially hidden

meditation_canvas = ctk.CTkCanvas(meditation_frame, width=screen_width, height=screen_height, bg="#242424")
meditation_canvas.grid(row=0, column=0, sticky="nsew")

meditation_frame.grid_rowconfigure(0, weight=1)
meditation_frame.grid_columnconfigure(0, weight=1)

circle = meditation_canvas.create_oval(
    center_x - radius, center_y - radius,
    center_x + radius, center_y + radius,
    fill="#3B8EEA", outline="", width=0
)

message_label = ctk.CTkLabel(meditation_frame, text="", bg_color="#242424")
message_label.place(x=35, y=50)

start_meditation_button = ctk.CTkButton(meditation_frame, text="Start Meditation", command=start_meditation)
start_meditation_button.grid(row=0, column=0, padx=35, pady=150)

stop_meditation_button = ctk.CTkButton(meditation_frame, text="Stop Meditation", command=terminate_meditation)
stop_meditation_button.grid(row=1, column=0, padx=35, pady=10)

root.mainloop()