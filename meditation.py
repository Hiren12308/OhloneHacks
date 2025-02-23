import customtkinter as ctk

root = ctk.CTk()

# Screen size
adjusted_screenwidth = (root.winfo_screenwidth()) * 0.8
adjusted_screenheight = (root.winfo_screenheight()) * 0.8

# Flag for stop button
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
radius_increment = (max_radius - min_radius) / (box_stage_duration_seconds * frames_per_second)

def render_circle_stage(stage_name, radius, radius_increment, duration_milliseconds):
    if stop: return
    duration_milliseconds -= frame_duration_milliseconds
    if duration_milliseconds < 0:
        return
    message_label.configure(text = stage_name)
    canvas.coords(circle, center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    radius += radius_increment
    root.after(frame_duration_milliseconds, render_circle_stage, stage_name, radius, radius_increment, duration_milliseconds)

def render_circle():
    if stop: return

    # Inhale stage
    stage_start_milliseconds = 0
    root.after(stage_start_milliseconds, render_circle_stage, "Breath in...", min_radius, radius_increment, box_stage_duration_milliseconds)

    # Inhale-Hold stage
    stage_start_milliseconds += box_stage_duration_milliseconds
    root.after(stage_start_milliseconds, render_circle_stage, "Hold...", max_radius, 0, box_stage_duration_milliseconds)

    # Exhale stage
    stage_start_milliseconds += box_stage_duration_milliseconds
    root.after(stage_start_milliseconds, render_circle_stage, "Breath out...", max_radius, -radius_increment, box_stage_duration_milliseconds)

    # Exhale-Hold stage
    stage_start_milliseconds += box_stage_duration_milliseconds
    root.after(stage_start_milliseconds, render_circle_stage, "Hold...", min_radius, 0, box_stage_duration_milliseconds)

    # Repeat again
    stage_start_milliseconds += box_stage_duration_milliseconds
    root.after(stage_start_milliseconds, render_circle)

def start_meditation():
    global stop
    stop = False

    render_circle()
    # if index < len(sequence):
    #     count, message = sequence[index]
    #     countdown(count, message, lambda: run_countdowns(sequence, index + 1))

def terminate_meditation():
    global stop
    stop = True

# Other objects and things
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

start_meditation_button = ctk.CTkButton(root, text="Start Meditation", command=start_meditation)
start_meditation_button.grid(row=0, column=0, padx=35, pady=150)

stop_meditation_button = ctk.CTkButton(root, text="Stop Meditation", command=terminate_meditation)
stop_meditation_button.grid(row=1, column=0, padx=35, pady=10)

root.mainloop()