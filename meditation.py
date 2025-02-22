import tkinter as tk

def countdown(count, message, on_complete=None):
    label['text'] = count
    message_label['text'] = message

    if count > 0:
        # Call countdown again after 1 second
        window.after(1000, countdown, count - 1, message, on_complete)
    else:
        # When countdown finishes, do the callback
        if on_complete:
            on_complete()

def run_countdowns(sequence, index=0):
    if index < len(sequence):
        count, message = sequence[index]
        countdown(count, message, lambda: run_countdowns(sequence, index + 1))

# The sequence of the countdowns as well as what text will display
sequence = [
    (4, "Breathe in..."),
    (4, "Hold..."),
    (4, "Breathe out..."),
    (4, "Hold...")
]

window = tk.Tk()

label = tk.Label(window)
label.place(x=35, y=15)

message_label = tk.Label(window)
message_label.place(x=35, y=50)

# Start the countdowns
run_countdowns(sequence)

window.mainloop()