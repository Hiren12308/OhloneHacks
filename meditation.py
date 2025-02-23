import customtkinter as ctk

root = ctk.CTk()

# Screen size
adjusted_screenwidth = (root.winfo_screenwidth()) * 0.8
adjusted_screenheight = (root.winfo_screenheight()) * 0.8

# Flag for stop button
stop_countdown = False

# For the expanding circle
pause = False

growing = True 
center_x = 200
center_y = 200
radius = 10
max_radius = 100
min_radius = 10

animation_duration = 4000
time_step = 40
steps_per_cycle = animation_duration // time_step
radius_step = (max_radius - min_radius) / steps_per_cycle

# Functions:
def animate_circle():
    global radius, growing, pause

    if pause:
        root.after(4000, resume_growth)
        return

    if growing:
        radius += radius_step
    else:
        radius -= radius_step

    canvas.coords(circle, center_x - radius, center_y - radius, center_x + radius, center_y + radius)

    if radius >= max_radius:
        growing = False
        pause = True
        root.after(4000, animate_circle)
    elif radius <= min_radius:
        growing = True
        pause = True
        root.after(4000, animate_circle)
    else:
        root.after(time_step, animate_circle)

def resume_growth():
    global pause
    pause = False
    animate_circle()

def countdown(count, message, on_complete=None):
    global stop_countdown
    if stop_countdown:
        stop_countdown = False
        return

    label.configure(text=count)
    message_label.configure(text=message)

    if count >= 1:
        root.after(1000, countdown, count - 1, message, on_complete)
    else:
        if on_complete:
            on_complete()

def run_countdowns(sequence, index=0):
    global stop_countdown
    stop_countdown = False

    animate_circle()
    if index < len(sequence):
        count, message = sequence[index]
        countdown(count, message, lambda: run_countdowns(sequence, index + 1))

def terminate_meditation():
    global stop_countdown
    stop_countdown = True

# Other objects and things
sequence = [
    (4, "Breathe in..."),
    (4, "Hold..."),
    (4, "Breathe out..."),
    (4, "Hold...")
]

root.geometry(f"{adjusted_screenwidth}x{adjusted_screenheight}")

canvas = ctk.CTkCanvas(root, width=adjusted_screenwidth, height=adjusted_screenheight, bg="#242424")
canvas.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

circle = canvas.create_oval(
    center_x - radius, center_y - radius,
    center_x + radius, center_y + radius,
    fill="#3B8EEA", outline="", width=0
)

label = ctk.CTkLabel(root, text="")
label.place(x=35, y=15)

message_label = ctk.CTkLabel(root, text="")
message_label.place(x=35, y=50)

start_meditation = ctk.CTkButton(root, text="Start Meditation", command=lambda: run_countdowns(sequence))
start_meditation.grid(row=0, column=0, padx=35, pady=150)

stop_meditation = ctk.CTkButton(root, text="Stop Meditation", command=terminate_meditation)
stop_meditation.grid(row=1, column=0, padx=35, pady=10)

root.mainloop()