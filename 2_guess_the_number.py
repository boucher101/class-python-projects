# template for "Guess the number" project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import tkinter
import random
import math

game_range = 100
secret_number = 0
remaining_guesses = 7


# helper function to start and restart the game
def new_game():
    global secret_number, remaining_guesses
    remaining_guesses = int(math.ceil(math.log(game_range + 1, 2)))
    secret_number = random.randrange(0, game_range)
    print ("New game. Range is [0," + str(game_range) + ")")
    print ("Number of remaining guesses is", remaining_guesses)
    print ("")
   
# define event handlers for control panel
def range100():
    global game_range, remaining_guesses
    game_range = 100
    #remaining_guesses = 7
    new_game()

def range1000():
    global game_range, remaining_guess
    game_range = 1000
    #remaining_guesses = 10
    new_game()
    
def input_guess(guess):
    global remaining_guesses
    int_guess = int(guess)
    
    print ("Guess was", int_guess)
    
    remaining_guesses = remaining_guesses - 1
    
    print ("Number of remaining guesses is", remaining_guesses)

    entry.delete(first=0, last=5)

    if remaining_guesses == 0 and int_guess != secret_number:
        print ("You ran out of guesses. The number was", secret_number)
        print ("")
        new_game()
    elif int_guess == secret_number:
        print ("Correct!\n")
        new_game()
    elif int_guess > secret_number:
        print ("Lower!\n")
    else:
        print ("Higher!\n")
        

def quit():
    root.destroy()

    
new_game()

# create frame
root = tkinter.Tk()
root.title("Guess the Number")
frame = tkinter.Frame(root, height = 200, width = 200)
frame.pack()

label=tkinter.Label(frame, text='Guess')
label.grid(row=0, column = 0)
entry = tkinter.Entry(frame, width = 5)
entry.grid(row=0, column = 1)
btn0 = tkinter.Button(frame, text='Submit', command=lambda: input_guess(entry.get()))
btn0.grid(row=0, column=2)
btn1 = tkinter.Button(frame, text='Range is [0,100)', command=range100)
btn1.grid(row=1, column=0, columnspan=2)
btn2 = tkinter.Button(frame, text='Range is [0,1000)', command=range1000)
btn2.grid(row=2, column=0, columnspan=2)

quit_btn = tkinter.Button(frame, text = 'Quit', command = quit)
quit_btn.grid(row = 3, column = 0)

# register event handlers for control elements and start frame

root.mainloop()

