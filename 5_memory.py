# implementation of card game - Memory

import tkinter
import random

# helper function to initialize globals
def new_game():
    global deck, exposed, state, card1, card2, turns
 #   deck = list(range(8)) + list(range(8))
    deck = list(range(8))* 2
    print(deck)
    random.shuffle(deck)
    exposed = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
    print(exposed)
    state = 0
    card1 = 0
    card2 = 0
    turns = 0
    label.configure(text='Turns = 0')
    draw()
     
# define event handlers
def mouseclick(event):
    global state, card1, card2, turns
    card_pos = event.x // 50
    if not exposed[card_pos]:
        exposed[card_pos] = True
        if state == 0:
            card1 = card_pos
            state = 1
        elif state == 1:
            card2 = card_pos
            state = 2
            turns +=1 
            label.config(text='Turns = ' + str(turns))
        else:
            if deck[card1] != deck[card2]:
                exposed[card1] = False 
                exposed[card2] = False
            card1 = card_pos
            state = 1
    draw()
    
                        
# cards are logically 50x100 pixels in size    
def draw():
    canvas.delete('all')
    n = 0
    for card in deck:
        if exposed[n]:
            canvas.create_rectangle(n*50, 0, (n+1)*50, 99)
            canvas.create_text((n+1)*50-25, 50, text=str(card), fill='Red', font=("Verdana", 36))
        else:
            canvas.create_rectangle(n*50, 0, (n+1)*50, 99, fill='Green', width=1)
        n += 1


# create frame and add a button and labels
root = tkinter.Tk()
root.title('Memory')
frame = tkinter.Frame(root, width=800, height=100)
frame.pack()
canvas = tkinter.Canvas(frame, width=800, height=100, highlightthickness=0)
canvas.pack()
tkinter.Button(frame, text='Reset', command=new_game).pack()
label=tkinter.Label(frame, text='Turns = 0')
label.pack()

# register event handlers
canvas.bind_all("<Button-1>", mouseclick)

# get things rolling
new_game()
draw()
root.mainloop()
