import customtkinter as ctk
import random
from tkinter import Canvas

# Initialize window
root = ctk.CTk()
root.title("Exercise")

height = int(root.winfo_screenheight() * 0.8)
width = int(root.winfo_screenwidth() * 0.8)
root.geometry(f"{width}x{height}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Use Tkinter's Canvas
canvas = Canvas(root, width=width, height=height, bg="#00008B", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Sentences to reveal
exercises = [
    "Get some snacks", "Drink water", "Stretch", "Walk around", "Take a break",
    "Watch some videos", "Exercise", "Meditate", "Listen to music", "Take a nap",
    "Call a friend", "Game for a bit", "Change your environment"
]

# Set number of circles dynamically (e.g., 75% of exercise list)
num_circles = max(len(exercises) * 3 // 4, 5)  # Ensures at least 5 circles

# Store circles, their movement speeds, and associated text IDs
circles = {}
speeds = {}

# Create moving circles
for _ in range(num_circles):
    while True:  # Prevents overlapping circles at start
        x, y = random.randint(50, width - 100), random.randint(50, height - 100)
        circle = canvas.create_oval(x, y, x + 50, y + 50, fill="red", outline="black")
        
        if circle:  # Ensure valid ID
            text_id = canvas.create_text((x + x + 50) / 2, (y + y + 50) / 2, text="", font=("Arial", 20), fill="white")
            circles[circle] = text_id
            speeds[circle] = (random.randint(1, 5), random.randint(1, 5))
            break  # Exit loop when circle is successfully created

# Move circles and associated text
def move_circles():
    for circle, text_id in circles.items():
        coords = canvas.coords(circle)
        if not coords:
            continue

        x1, y1, x2, y2 = coords
        dx, dy = speeds[circle]

        # Reverse direction at edges
        if x2 > width or x1 < 0:
            dx = -dx
        if y2 > height or y1 < 0:
            dy = -dy

        # Move circle and its associated text
        canvas.move(circle, dx, dy)
        canvas.move(text_id, dx, dy)
        speeds[circle] = (dx, dy)

    root.after(50, move_circles)

# Handle circle clicks
def on_click(event):
    for circle, text_id in circles.items():
        x1, y1, x2, y2 = canvas.coords(circle)
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            sentence = random.choice(exercises)
            canvas.itemconfig(text_id, text=sentence)  # Update text inside the circle
            break  # Stop checking after one match

# Bind click event
canvas.bind("<Button-1>", on_click)

# Start movement
move_circles()

root.mainloop()
