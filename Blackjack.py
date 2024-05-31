"""
BLACKJACK GAME USING OOP AND TKINTER IN PYTHON

## Game Play:
To play a hand of Blackjack the following steps must be followed:
1. Create a deck of 52 cards
2. Shuffle the deck
3. Ask the Player for their bet
4. Make sure that the Player's bet does not exceed their available chips
5. Deal two cards to the Dealer and two cards to the Player
6. Show only one of the Dealer's cards, the other remains hidden
7. Show both of the Player's cards
8. Ask the Player if they wish to Hit, and take another card
9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
10. If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
11. Determine the winner and adjust the Player's chips accordingly
12. Ask the Player if they'd like to play again

"""

import random
import tkinter as tk
from tkinter import messagebox

# Global variables for suits, ranks and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Card class for creating the card object
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

# Deck class for instantiating and shuffling 52 unique card objects
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank)) # building a card and adding it to the list
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Hand class for holding the card object and calculating the value of those cards
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    # If Hand's value exceeds 21 and we have an Ace, we can reduce the value of Ace to 1
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Chip class for keeping track of player's starting chips, bets and ongoing winnings
class Chip:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# Initializing the GUI
root = tk.Tk()
root.title("Blackjack Game")

deck = Deck() # creating a deck

player_hand = Hand() 
dealer_hand = Hand() 

chip_count = Chip() # setting up player chips

# Function for taking bets 
def take_bet():
    try:
        bet = int(bet_entry.get())
        if bet <= chip_count.total:
            chip_count.bet = bet
            return True
        else:
            messagebox.showerror("Error", "Bet exceeds total chips!")
            return False
    except ValueError:
        messagebox.showerror("Error", "Invalid input!")
        return False

# Function for dealing two cards to the player and the dealer
def deal_initial():
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

def display_cards():
    player_cards_label.config(text="Player's Hand:\n" + '\n'.join(str(card) for card in player_hand.cards))
    dealer_cards_label.config(text="Dealer's Hand:\n" + str(dealer_hand.cards[0]) + '\n <card hidden>')

def update_chip_count():
    chip_count_label.config(text="Chips: " + str(chip_count.total))

def ask_play_again():
    new_game = messagebox.askyesno("Play Again?", "Would you like to play another hand?")
    if new_game:
        reset_game()
    else:
        root.destroy()

# Function for Hit
def hit():
    player_hand.add_card(deck.deal())
    player_hand.adjust_for_ace()
    display_cards()
    if player_hand.value > 21:
        player_busts()

# Function for Stand
def stand():
    dealer_turn()

def player_busts():
    messagebox.showinfo("Result", f"Player busts! \n\n Hidden Card - {dealer_hand.cards[1]} \n\n Dealer Hand value = {dealer_hand.value} \n Player Hand value = {player_hand.value}")
    chip_count.lose_bet()
    update_chip_count()
    ask_play_again()    

def dealer_turn():
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())
        dealer_hand.adjust_for_ace()
        display_cards()

    if dealer_hand.value > 21 or dealer_hand.value < player_hand.value:
        player_wins()
    elif dealer_hand.value > player_hand.value:
        dealer_wins()
    else:
        messagebox.showinfo("Result", f"It's a tie! \n\n Hidden Card - {dealer_hand.cards[1]} \n\n Dealer Hand value = {dealer_hand.value} \n Player Hand value = {player_hand.value}")
        ask_play_again()

def player_wins():
    messagebox.showinfo("Result", f"Player wins! \n\n Hidden Card - {dealer_hand.cards[1]} \n\n Dealer Hand value = {dealer_hand.value} \n Player Hand value = {player_hand.value}")
    chip_count.win_bet()
    update_chip_count()
    ask_play_again()

def dealer_wins():
    messagebox.showinfo("Result", f"Dealer wins! \n\n Hidden Card - {dealer_hand.cards[1]} \n\n Dealer Hand value = {dealer_hand.value} \n Player Hand value = {player_hand.value}")
    chip_count.lose_bet()
    update_chip_count()
    ask_play_again()

def reset_game():
    global player_hand
    global dealer_hand
    global chip_count
    global deck
    global playing

    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    chip_count.bet = 0
    chip_count_label.config(text="Chips: " + str(chip_count.total))
    result_label.config(text="")
    start_game()

def start_game():
    if take_bet():
        deal_initial()
        display_cards()
        hit_button.config(state="normal")
        stand_button.config(state="normal")

# Create Tkinter elements
bet_label = tk.Label(root, text="Enter bet:", fg="blue", font=("Arial", 11))
bet_entry = tk.Entry(root)
start_button = tk.Button(root, text="Start Game", command=start_game, bg="green", fg="white", font=("Arial", 10, "bold"))
hit_button = tk.Button(root, text="Hit", command=hit, state="disabled", bg="red", fg="white", font=("Arial", 10))
stand_button = tk.Button(root, text="Stand", command=stand, state="disabled", bg="orange", fg="white", font=("Arial", 10))
player_cards_label = tk.Label(root, text="Player's Hand:", fg="black", font=("Arial", 10, "italic"))
dealer_cards_label = tk.Label(root, text="Dealer's Hand:", fg="black", font=("Arial", 10, "italic"))
result_label = tk.Label(root, text="", fg="purple", font=("Arial", 11))
chip_count_label = tk.Label(root, text="Chips: 100", fg="brown", font=("Arial", 11))

# Layout GUI elements
bet_label.grid(row=0, column=0)
bet_entry.grid(row=0, column=1)
start_button.grid(row=0, column=2)
hit_button.grid(row=1, column=0)
stand_button.grid(row=1, column=1)
player_cards_label.grid(row=2, column=0)
dealer_cards_label.grid(row=2, column=1)
result_label.grid(row=3, column=0, columnspan=2)
chip_count_label.grid(row=4, column=0, columnspan=2)

# Run the GUI main loop
root.mainloop()
