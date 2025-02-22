import customtkinter as ctk
import tkinter as tk

stop_countdown = False

def countdown(count, message, on_complete=None):
    global stop_countdown

    if stop_countdown:
        stop_countdown = False
        return

    label.configure(text=count)
    message_label.configure(text=message)

    if count >= 0:
        window.after(1000, countdown, count - 1, message, on_complete)
        meditation_progress_bar.start()
    else:
        if on_complete:
            on_complete()

def run_countdowns(sequence, index=0):
    global stop_countdown
    stop_countdown = False
    if index < len(sequence):
        count, message = sequence[index]
        countdown(count, message, lambda: run_countdowns(sequence, index + 1))

def terminate_meditation():
    global stop_countdown
    stop_countdown = True

sequence = [
    (4, "Breathe in..."),
    (4, "Hold..."),
    (4, "Breathe out..."),
    (4, "Hold...")
]

window = ctk.CTk()

label = ctk.CTkLabel(window, text="")
label.place(x=35, y=15)

message_label = ctk.CTkLabel(window, text="")
message_label.place(x=35, y=50)

start_meditation = ctk.CTkButton(window, text="Start Meditation", command=lambda: run_countdowns(sequence))
stop_meditation = ctk.CTkButton(window, text="Stop Meditation", command=lambda: terminate_meditation())
start_meditation.grid(row=0, column=0, padx=35, pady=150)
stop_meditation.grid(row=1, column=0, padx=35, pady=10)

meditation_progress_bar = ctk.CTkProgressBar(window, orientation = "horizontal", indeterminate_speed=0.5)
meditation_progress_bar.set(0)
meditation_progress_bar.place(x=35, y=75)

window.mainloop()