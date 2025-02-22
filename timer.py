import time
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import math

root = Tk()

root.geometry("1000x1000")
root.title("Timer")

hour = StringVar()
minute = StringVar()
second = StringVar()

hour.set("00")
minute.set("05")
second.set("00")

def relax():
    hour.set("00")
    minute.set("5")
    second.set("00")

hourEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=hour, state='readonly')
hourEntry.place(x=80, y=20)
minuteEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=minute, state='readonly')
minuteEntry.place(x=130, y=20)
secondEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=second, state='readonly')
secondEntry.place(x=180, y=20)

canvas = Canvas(root, width=150, height=150, bg='white', highlightthickness=0)
canvas.place(x=75, y=60)
canvas.create_oval(25, 25, 125, 125, outline='gray', width=5)

def countdown():
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get()) 
        total_time = temp

        if temp < 0:
            messagebox.showerror("Error", "Invalid time input!")
            return
        
        btn.config(state=DISABLED)
        
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
                
                start_rad = math.radians(start_angle)
                end_rad = math.radians(end_angle)
                
                canvas.delete("progress")
                canvas.create_arc(25, 25, 125, 125, 
                                start=start_angle, 
                                extent=-angle,
                                outline='blue', 
                                width=5, 
                                style=ARC,
                                tags="progress")

                if temp > 0:
                    temp -= 1
                    root.after(1000, update_timer)
                else:
                    messagebox.showinfo("Time Countdown", "Time's up!")
                    btn.config(state=NORMAL)
                    Relaxbtn = Button(root, text='Relax', bd='5', command=relax)
                    Relaxbtn.place(x=70, y=212)
                    
            else:
                messagebox.showinfo("Error", "Invalid time input!")
                btn.config(state=NORMAL)

        update_timer()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        btn.config(state=NORMAL)

btn = Button(root, text='Set Time Countdown', bd='5', command=countdown)
btn.place(x=70, y=212)

root.mainloop()