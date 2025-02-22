# import tkinter as tk

# def countdown(count, message, on_complete=None):
#     label['text'] = count
#     message_label['text'] = message

#     if count > 0:
#         # Call countdown again after 1 second
#         window.after(1000, countdown, count - 1, message, on_complete)
#     else:
#         # When countdown finishes, do the callback
#         if on_complete:
#             on_complete()

# def run_countdowns(sequence, index=0):
#     if index < len(sequence):
#         count, message = sequence[index]
#         countdown(count, message, lambda: run_countdowns(sequence, index + 1))

# # The sequence of the countdowns as well as what text will display
# sequence = [
#     (4, "Breathe in..."),
#     (4, "Hold..."),
#     (4, "Breathe out..."),
#     (4, "Hold...")
# ]

# window = tk.Tk()

# label = tk.Label(window)
# label.place(x=35, y=15)

# message_label = tk.Label(window)
# message_label.place(x=35, y=50)

# slider = tk.Scale(window, from_=0, to=4, orient="vertical", length=100)
# slider.place(x=35, y=100)

# # Start the countdowns
# run_countdowns(sequence)

# window.mainloop()

import tkinter as tk

def countdown(count, message, on_complete=None):
    label['text'] = count
    message_label['text'] = message

    new_width = initial_width + ((4 - count) * 10) 
    canvas.coords(rect, initial_x, initial_y, new_width, rect_height)  # Update rectangle

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

window = tk.Tk()

label = tk.Label(window)
label.place(x=35, y=15)

message_label = tk.Label(window)
message_label.place(x=35, y=50)

canvas = tk.Canvas(window, width=400, height=200)
canvas.place(x=35, y=100)

# Initial rectangle parameters
initial_x = 35
initial_y = 50
rect_height = 40
initial_width = 50

# Create the rectangle
rect = canvas.create_rectangle(initial_x, initial_y, initial_x + initial_width, initial_y + rect_height, fill="red")

# Start the countdowns

run_countdowns(sequence)

window.mainloop()