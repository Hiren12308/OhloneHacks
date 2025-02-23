import customtkinter as ctk

stop_countdown = False

def countdown(count, message, current_bar = "left", on_complete=None):
    global stop_countdown
    if stop_countdown:
        stop_countdown = False
        left_bar.stop()
        return

    label.configure(text=count)
    message_label.configure(text=message)

    if current_bar == "left":
        bottom_bar.stop()
        left_bar.start()
    if current_bar == "top":
        left_bar.stop()
        top_bar.start()
    if current_bar == "right":
        top_bar.stop()
        right_bar.start()
    if current_bar == "bottom":
        right_bar.stop()
        bottom_bar.start()

    if count >= 1:
        root.after(1000, countdown, count - 1, message, current_bar, on_complete)
    else:
        if on_complete:
            on_complete()

def run_countdowns(sequence, index=0):
    global stop_countdown
    stop_countdown = False

    if index < len(sequence):
        count, message, current_bar = sequence[index]
        countdown(count, message, current_bar, lambda: run_countdowns(sequence, index + 1))

def terminate_meditation():
    global stop_countdown
    stop_countdown = True

sequence = [
    (4, "Breathe in...", "left"),
    (4, "Hold...", "top"),
    (4, "Breathe out...", "right"),
    (4, "Hold...", "bottom")
]

root = ctk.CTk()

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

root.geometry(f"{int(screenwidth * 0.8)}x{int(screenheight * 0.8)}")

label = ctk.CTkLabel(root, text="")
label.place(x=35, y=15)

message_label = ctk.CTkLabel(root, text="")
message_label.place(x=35, y=50)

start_meditation = ctk.CTkButton(root, text="Start Meditation", command=lambda: run_countdowns(sequence) )
start_meditation.grid(row=0, column=0, padx=35, pady=150)

stop_meditation = ctk.CTkButton(root, text="Stop Meditation", command=terminate_meditation)
stop_meditation.grid(row=1, column=0, padx=35, pady=10)

bar_speed = 0.262
length = 500

left_bar = ctk.CTkProgressBar(root, orientation="vertical", determinate_speed=bar_speed, height=length)
left_bar.set(0)
left_bar.place(x=35, y=75)

top_bar = ctk.CTkProgressBar(root, orientation="horizontal", determinate_speed=bar_speed, width=length)
top_bar.set(0)
top_bar.place(x=35, y=75)

right_bar = ctk.CTkProgressBar(root, orientation="vertical", determinate_speed=bar_speed, height=length)
right_bar.set(0)
right_bar.place(x=35+length, y=75)

bottom_bar = ctk.CTkProgressBar(root, orientation="horizontal", determinate_speed=bar_speed, width=length)
bottom_bar.set(0)
bottom_bar.place(x=35, y=75+length)

root.mainloop()