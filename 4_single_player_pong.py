import tkinter
import time
import random
from PIL import Image, ImageTk

# set global variables
WIDTH = 400
HEIGHT = 400
RADIUS = 20
PAD_WIDTH = 80
PAD_HEIGHT = 8
angle = 0

def spawn_ball():
    global direction, ball_pos, ball_vel
    
    # set starting ball position
    ball_pos = [WIDTH/2-RADIUS, HEIGHT/4-RADIUS, WIDTH/2+RADIUS, HEIGHT/4+RADIUS]

    # get random numbers for x and y coordinates of ball velocity
    ball_vel = [random.randrange(3, 5), random.randrange(2, 4)]

    # randomly choose if ball is spawned to right or left
    # if left, then 
    direction = random.choice(['LEFT', 'RIGHT'])
    if direction == 'LEFT':
        ball_vel[0] = -ball_vel[0]

    # call draw
    draw()
        

    
def new_game():
    global pad_vel, pad_pos
    global score, hit_bottom
    
    # set pad_vel and pad_pos
    pad_vel = 0
    pad_pos = [WIDTH/2-PAD_WIDTH/2, HEIGHT-PAD_HEIGHT, WIDTH/2+PAD_WIDTH/2, HEIGHT]

    # intialize score to 0 and hit_bottom to False
    score = 0
    hit_bottom = False

    # call spawn_ball
    spawn_ball()
       
def draw():
    global score, hit_bottom, pad_vel, angle
    canvas.delete('all')
    
    # draw gutter
    canvas.create_line(0, HEIGHT-PAD_HEIGHT, WIDTH, HEIGHT-PAD_HEIGHT)
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_pos[2] += ball_vel[0]
    ball_pos[3] += ball_vel[1]

    # draw ball
    canvas.create_oval(ball_pos, fill = 'Red')
    
    # update paddle's horizontal position, keep paddle on the screen
    if pad_pos[0] + pad_vel >= 0 and pad_pos[2] + pad_vel <= WIDTH:
        pad_pos[0] += pad_vel
        pad_pos[2] += pad_vel

    # draw paddle
    canvas.create_rectangle(pad_pos, fill = 'black')

    # determine whether ball collides with gutter
    # determine whether ball collides with paddle
    if ball_pos[3] >= HEIGHT - PAD_HEIGHT:
        if ball_pos[0] + RADIUS > pad_pos[0] and ball_pos[0] + RADIUS < pad_pos[2]:
            ball_vel[1] = -ball_vel[1] * 1.1
            score += 1
        else:
            hit_bottom = True

    # reflect ball off top and side walls        
    if ball_pos[1] <= 0:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
        ball_vel[0] = -ball_vel[0]
    
    # draw score
    canvas.create_text(WIDTH/2, 30, text = str(score), font = ("Verdana", 48))

    if not hit_bottom:
        root.after(10, draw)
    
def keydown(event):
    global pad_vel
    '''set velocity for paddle based on keys pressed'''
    if event.keysym == 'Left':
        pad_vel = -4
    elif event.keysym == 'Right':
        pad_vel = 4

def keyup(event):
    global pad_vel
    '''stop paddle when keys are released'''
    if event.keysym == 'Left' or event.keysym == 'Right':
        pad_vel = 0

# create Tk window and canvas
root = tkinter.Tk()
root.title('Pong')
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()

# set focus on canvas
canvas.focus_set()

# bind <Key> and <KeyRelease> events to appropriate event handlers
canvas.bind("<Key>", keydown)
canvas.bind("<KeyRelease>", keyup)

# start a new game
new_game()

# create while loop to draw and establish sleep for .01 seconds
root.mainloop()
##while not hit_bottom:
##    draw()
##    root.update_idletasks()
##    root.update()
##    time.sleep(0.01)
