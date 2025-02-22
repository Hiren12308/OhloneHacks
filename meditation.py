import customtkinter as ctk
import tkinter as tk

def countdown(count, message, on_complete=None):
    label.configure(text=count)
    message_label.configure(text=message)

    if count >= 0:
        window.after(1000, countdown, count - 1, message, on_complete)
    else:
        if on_complete:
            on_complete()

def run_countdowns(sequence, index=0):
    if index < len(sequence):
        count, message = sequence[index]
        countdown(count, message, lambda: run_countdowns(sequence, index + 1))

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

canvas = ctk.CTkCanvas(window, width=400, height=200)
canvas.place(x=35, y=100)

start_meditation = ctk.CTkButton(window, text="Start Meditation", command=lambda: run_countdowns(sequence))
start_meditation.place(x=35, y=150)

window.mainloop()