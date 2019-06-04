# Mini-project #6 - Blackjack

import tkinter
import random
from PIL import Image, ImageTk

# load card sprite - 936x384 - source: jfitz.com
card_images = Image.open("cards_jfitz.png")
card_back = Image.open("card_jfitz_back.png")

# initialize some useful global variables
WIDTH = 600
HEIGHT = 400
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
in_play = False
outcome = ""
score = 0
final = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.im = None
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, pos):

        r = RANKS.index(self.rank)
        s = SUITS.index(self.suit)
        
        card_loc = (r * CARD_SIZE[0], s * CARD_SIZE[1], (r + 1) * CARD_SIZE[0], (s + 1) * CARD_SIZE[1])

        self.im = ImageTk.PhotoImage(card_images.crop((card_loc)))
        canvas.create_image(pos, image = self.im)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand = "Hand contains "
        for card in self.cards:
            hand = hand + " " + str(card)
        return hand

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand
        value = 0
        ace = False
        for card in self.cards:
            value = value + VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace = True
        if ace and value <= 11:
            value = value + 10
        return value
        
    def draw(self, pos):
        # draw a hand on the canvas, use the card's draw method
        for card in self.cards:
            card.draw(pos)
            pos[0] = pos[0] + CARD_SIZE[0] + 5
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        # return a string representing the deck
        deck = "Deck contains "
        for card in self.deck:
            deck = deck + " " + card
        return deck
    
    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, final, score
    if in_play:
        score -= 1
        final = "Round not finished. You lose!"
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
        dealer = Hand()
        player = Hand()
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        outcome = "Hit or Stand?"
        final = ""
        in_play = True
    draw()

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global outcome, final, in_play, score
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            score -= 1
            final = "You busted. You lose!"
            outcome = "New Deal?"
            in_play = False
    draw()
        
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global final, in_play, outcome, score
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            final = "Dealer Busted. You win!"
            score += 1
        elif dealer.get_value() >= player.get_value():
            final = "Dealer wins!"
            score -= 1
        else:
            final = "You win!"
            score += 1
        outcome = "New Deal?"
        in_play = False
    draw()
        
# draw handler    
def draw():
    # test to make sure that card.draw works, replace with your code below
    canvas.delete('all')
    canvas.create_text(100, 30, text='Blackjack', font=('sans-serif', 36), fill='Red')
    canvas.create_text(100, 75, text='Dealer', font=('sans-serif', 24), fill='Black')
    canvas.create_text(100, 230, text='Player', font=('sans-serif', 24), fill='Black')
    canvas.create_text(400, 75, text=outcome, font=('sans-serif', 24), fill='Black')
    canvas.create_text(400, 230, text=final, font=('sans-serif', 24), fill='Black')
    canvas.create_text(450, 30, text="Score: " + str(score), font=('sans-serif', 24), fill='Black')
                      
    dealer.draw([100, 150])  # draw the dealer's cards starting from this location
    player.draw([100, 300])  # draw the player's cards starting from this location
    
    if in_play: # cover the dealer's first card if player is still playing hand
        im = ImageTk.PhotoImage(card_back.crop((1, 0, CARD_SIZE[0], CARD_SIZE[1])))
        canvas.create_image(100, 150, image = im)
        canvas.image = im

# initialization frame
root = tkinter.Tk()
root.title('Blackjack')
frame = tkinter.Frame(root)
frame.pack()
canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, highlightthickness=0, bg='Green')
canvas.grid(row=0, columnspan=3)

#create buttons and canvas callback
tkinter.Button(frame, text='Deal', width=10, command=deal).grid(row=1, column=0, sticky='E')
tkinter.Button(frame, text='Hit', width=10, command=hit).grid(row=1, column=1)
tkinter.Button(frame, text='Stand', width=10, command=stand).grid(row=1, column=2, sticky='W')
deal()


# get things rolling

root.mainloop()

