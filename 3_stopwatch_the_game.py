# import modules
import tkinter
import time

# declare global variables
timer_on = False
start_time = 0
elapsed_time = 0
wins = 0
attempts = 0

# helper functions
def format_score():
    return str(wins) + " / " + str(attempts)

def format_time(time_in_seconds):
    global tenth
    minute = int(time_in_seconds // 60)
    seconds = int(time_in_seconds % 60)
    tenth = int(time_in_seconds * 10) % 10
    if seconds < 10:
        zero = "0"
    else:
        zero = ""
    return str(minute)+":"+zero+str(seconds)+"."+str(tenth)

# event handler functions
def start():
    global start_time, timer_on
    if not timer_on:
        timer_on = True
        start_time = time.time() - elapsed_time
        tick()

def stop():
    global timer_on, wins, attempts
    if timer_on:
        timer_on = False
        attempts += 1
        if tenth == 0:
            wins += 1
        draw()

def reset():
    global timer_on, elapsed_time, start_time, wins, attempts
    timer_on = False
    elapsed_time = 0
    start_time = 0
    wins = 0
    attempts = 0
    draw()

def quit_timer():
    stop()
    root.destroy()
    
def tick():
    global elapsed_time
    if timer_on:
        elapsed_time = time.time() - start_time
        draw()
        root.after(100, tick)

# draw handler
def draw():
    canvas.delete('all')
    canvas.create_text(100, 100, text = format_time(elapsed_time), font=('Verdana', 36))
    canvas.create_text(150, 50, text = format_score())

# create frame
root = tkinter.Tk()
frame = tkinter.Frame(root, width = 300, height = 300)
frame.pack()

# register event handlers
tkinter.Button(frame, text = "Start", width=7, command=start).grid(row=0, column=0)
tkinter.Button(frame, text = "Stop", width=7, command=stop).grid(row=1, column=0)
tkinter.Button(frame, text = "Reset", width=7, command=reset).grid(row=2, column=0)
tkinter.Button(frame, text = "Quit", width =7, command=quit_timer).grid(row=3, column=0)

#canvas = tkinter.Canvas(frame, width = 200, height = 200, bg = "Yellow")
canvas = tkinter.Canvas(frame, width = 200, height = 200, bg = "Yellow", highlightthickness=0)
canvas.grid(row=0, column=2, rowspan=50)

draw()

# start mainloop
root.mainloop()
