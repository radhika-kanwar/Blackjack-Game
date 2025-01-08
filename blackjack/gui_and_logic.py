import tkinter as tk
from tkinter import messagebox
from game_classes import Deck, Hand, Chip

class BlackjackGUI:
    def __init__(self):
        # Initializing the game objects
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.chip_count = Chip()

        # Setting up the Tkinter root window
        self.root = tk.Tk()
        self.root.title("Blackjack Game")
        self.setup_ui()

    def setup_ui(self):
        # Creating the GUI elements
        self.bet_label = tk.Label(self.root, text="Enter bet:", fg="blue", font=("Arial", 11))
        self.bet_entry = tk.Entry(self.root)
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit, state="disabled", bg="red", fg="white", font=("Arial", 10))
        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand, state="disabled", bg="orange", fg="white", font=("Arial", 10))
        self.player_cards_label = tk.Label(self.root, text="Player's Hand:", fg="black", font=("Arial", 10, "italic"))
        self.dealer_cards_label = tk.Label(self.root, text="Dealer's Hand:", fg="black", font=("Arial", 10, "italic"))
        self.result_label = tk.Label(self.root, text="", fg="purple", font=("Arial", 11))
        self.chip_count_label = tk.Label(self.root, text=f"Chips: {self.chip_count.total}", fg="brown", font=("Arial", 11))

        # Layout of the GUI elements
        self.bet_label.grid(row=0, column=0)
        self.bet_entry.grid(row=0, column=1)
        self.start_button.grid(row=0, column=2)
        self.hit_button.grid(row=1, column=0)
        self.stand_button.grid(row=1, column=1)
        self.player_cards_label.grid(row=2, column=0)
        self.dealer_cards_label.grid(row=2, column=1)
        self.result_label.grid(row=3, column=0, columnspan=2)
        self.chip_count_label.grid(row=4, column=0, columnspan=2)

    def start_game(self):
        if self.take_bet():
            self.start_button.config(state="disabled")
            self.deal_initial()
            self.display_cards()
            self.hit_button.config(state="normal")
            self.stand_button.config(state="normal")

    def take_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0:
                messagebox.showerror("Error ⚠️", "Bet must be positive!")
                return False
            elif bet > self.chip_count.total:
                messagebox.showerror("Error ⚠️", "Bet exceeds total chips!")
                return False
            self.chip_count.bet = bet
            return True
        except ValueError:
            messagebox.showerror("Error ⚠️", "Invalid input!")
            return False

    def deal_initial(self):
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

    def display_cards(self):
        self.player_cards_label.config(text="Player's Hand:\n" + '\n'.join(str(card) for card in self.player_hand.cards))
        self.dealer_cards_label.config(text="Dealer's Hand:\n" + str(self.dealer_hand.cards[0]) + "\n<card hidden 🎴>")

    def hit(self):
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.adjust_for_ace()
        self.display_cards()

        if self.player_hand.value > 21:
            self.player_busts()

    def stand(self):
        self.dealer_turn()

    def player_busts(self):
        messagebox.showinfo(
            "Result",
            f"Player busts! \nDealer's hidden card: {self.dealer_hand.cards[1]}",
        )
        self.chip_count.lose_bet()
        self.update_chip_count()
        if self.chip_count.total == 0:
            self.check_chips()
        else:
            self.ask_play_again()

    def dealer_turn(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_hand.adjust_for_ace()
        self.display_cards()

        if self.dealer_hand.value > 21 or self.player_hand.value > self.dealer_hand.value:
            self.player_wins()
        elif self.dealer_hand.value > self.player_hand.value:
            self.dealer_wins()
        else:
            messagebox.showinfo("Result", f"It's a tie! 🤝\n\n Hidden Card - {self.dealer_hand.cards[1]} \n\n Dealer Hand value = {self.dealer_hand.value} \n Player Hand value = {self.player_hand.value}")
            self.ask_play_again()

    def player_wins(self):
        messagebox.showinfo("Result", f"Player wins! 🎉\n\n Hidden Card - {self.dealer_hand.cards[1]} \n\n Dealer Hand value = {self.dealer_hand.value} \n Player Hand value = {self.player_hand.value}")
        self.chip_count.win_bet()
        self.update_chip_count()
        self.ask_play_again()

    def dealer_wins(self):
        messagebox.showinfo("Result", f"Dealer wins! 💥\n\n Hidden Card - {self.dealer_hand.cards[1]} \n\n Dealer Hand value = {self.dealer_hand.value} \n Player Hand value = {self.player_hand.value}")
        self.chip_count.lose_bet()
        self.update_chip_count()
        if self.chip_count.total == 0:
            self.check_chips()
        else:
            self.ask_play_again()

    def update_chip_count(self):
        self.chip_count_label.config(text=f"Chips: {self.chip_count.total}")

    def ask_play_again(self):
        if messagebox.askyesno("Play Again?", "Would you like to play another hand?"):
            self.reset_game()
        else:
            self.root.destroy()

    def check_chips(self):
        messagebox.showinfo("Game Over", "You have run out of chips! 😢")
        self.root.destroy()

    def reset_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck = Deck()
        self.deck.shuffle()

        self.chip_count.bet = 0
        self.update_chip_count()

        self.player_cards_label.config(text="Player's Hand:")
        self.dealer_cards_label.config(text="Dealer's Hand:")
        self.bet_entry.delete(0, tk.END)
        self.start_button.config(state="normal")
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def run(self):
        self.root.mainloop()