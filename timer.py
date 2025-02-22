import time
import customtkinter as ctk
import math

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x1000")
root.title("Timer")

hour = ctk.StringVar(value="00")
minute = ctk.StringVar(value="05")
second = ctk.StringVar(value="00")

def relax():
    hour.set("00")
    minute.set("5")
    second.set("00")

# Configure grid weights for root (simplified since labels are now on canvas)
root.grid_rowconfigure(0, weight=1)  # Space above canvas
root.grid_rowconfigure(1, weight=0)  # Canvas row
root.grid_rowconfigure(2, weight=1)  # Button row
root.grid_columnconfigure(0, weight=1)  # Center horizontally

# Canvas setup
canvas_size = int(min(root.winfo_screenwidth(), root.winfo_screenheight()) * 0.6)
canvas = ctk.CTkCanvas(master=root, width=canvas_size, height=canvas_size, 
                      bg=root.cget('bg'), highlightthickness=0)
canvas.grid(row=1, column=0, pady=20)

# Circle dimensions
padding = 25
circle_size = canvas_size - 2 * padding
canvas.create_oval(padding, padding, circle_size + padding, circle_size + padding, 
                  outline='gray', width=5)

# Place labels inside the circle (centered)
center_x = canvas_size / 2
center_y = canvas_size / 2

hourLabel = ctk.CTkLabel(master=canvas, textvariable=hour, font=("Arial", 35))
hourLabel.place(x=center_x - 70, y=center_y - 20, anchor="center")

colonLabel1 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", 35))
colonLabel1.place(x=center_x - 25, y=center_y - 20, anchor="center")

minuteLabel = ctk.CTkLabel(master=canvas, textvariable=minute, font=("Arial", 35))
minuteLabel.place(x=center_x, y=center_y - 20, anchor="center")

colonLabel2 = ctk.CTkLabel(master=canvas, text=":", font=("Arial", 35))
colonLabel2.place(x=center_x + 25, y=center_y - 20, anchor="center")

secondLabel = ctk.CTkLabel(master=canvas, textvariable=second, font=("Arial", 35))
secondLabel.place(x=center_x + 70, y=center_y - 20, anchor="center")

def countdown():
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
        total_time = temp

        if temp < 0:
            ctk.CTkMessageBox(master=root, title="Error", 
                            message="Invalid time input!", 
                            icon="cancel").show()
            return
        
        btn.configure(state="disabled")
        canvas.delete("progress")

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
                
                canvas.delete("progress")
                canvas.create_arc(padding, padding, circle_size + padding - 20, 
                                circle_size + padding - 20,
                                start=start_angle,
                                extent=-angle,
                                outline='blue',
                                width=5,
                                style="arc",
                                tags="progress")

                if temp > 0:
                    temp -= 1
                    root.after(1000, update_timer)
                else:
                    ctk.CTkMessageBox(master=root, title="Time Countdown",
                                   message="Time's up!",
                                   icon="info").show()
                    btn.configure(state="normal")
                    relax_btn = ctk.CTkButton(master=root, text="Relax",
                                            command=relax)
                    relax_btn.grid(row=2, column=0, pady=20)
                    
            else:
                ctk.CTkMessageBox(master=root, title="Error",
                               message="Invalid time input!",
                               icon="cancel").show()
                btn.configure(state="normal")

        update_timer()

    except ValueError:
        ctk.CTkMessageBox(master=root, title="Invalid Input",
                         message="Please enter valid numbers.",
                         icon="cancel").show()
        btn.configure(state="normal")

# Button using grid
btn = ctk.CTkButton(master=root, text="Set Time Countdown", command=countdown)
btn.grid(row=2, column=0, pady=20)

root.mainloop()