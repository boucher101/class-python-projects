
# Rock-paper-scissors template

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors" to numbers as follows:
#
# 1 - rock
# 2 - paper
# 3 - scissors

import random
import tkinter

# helper functions

def name_to_number(name):
    if name == "rock":
        return 1
    elif name == "paper":
        return 2
    elif name == "scissors":
        return 3
    else:
        return "Invalid choice"


def number_to_name(number):
    if number == 1:
        return "rock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "scissors"
    else:
        return "Number not in range"
    return "rock"
    

def rps(player_choice): 
    
    print ("")

    # print out the message for the player's choice
    print ("Player chooses " + player_choice)

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(1, 4)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print ("Computer chooses " + comp_choice)

    # compute difference of comp_number and player_number modulo three
    remainder = (comp_number - player_number) % 3

    # use if/elif/else to determine winner, print winner message
    if remainder == 1:
        print ("COMPUTER WINS!")
    elif remainder == 2:
        print ("PLAYER WINS!")
    else:
        print ("IT'S A TIE!")

def rock():
    rps("rock")

def paper():
    rps("paper")

def scissors():
    rps("scissors")

root = tkinter.Tk()
root.title("RPS")
frame = tkinter.Frame(root, width=100, height=100)
frame.pack()

tkinter.Button(frame, text="rock", height = 3, width = 7, command=rock).pack()
tkinter.Button(frame, text="paper", height = 3, width = 7, command=paper).pack()
tkinter.Button(frame, text="scissors", height = 3, width = 7, command=scissors).pack()

root.mainloop()
#rps("rock")
#rps("paper")
#rps("scissors")

##continue_game = "yes"
##while continue_game == "yes":
##    # ask the player to enter a choice
##    p1 = input("Enter your choice (rock, paper, scissors): ")
##
##    # then call the function rps() with the players choice
##    rps(p1)
##
##    print()
##    continue_game = input("Do you want to play again? (yes or no): ")
##    print()
