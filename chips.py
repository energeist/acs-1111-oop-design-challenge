from cards import Deck
from cards import Hand

class chips:
    def __init__(self, amount=3000, bet=0):
        self.amount = amount
        self.bet = bet
        self.money_in_wallet = 0

    def win_round(self, bet):
        self.total += bet
        self.money_in_wallet += 1

    def lose_round(self, bet):
        self.total -= bet 
        self.money_in_wallet -= 1

    def get_bet(chips):
        while True:
            if chips.bet:
                int(input("How much would you like to bet? "))
            elif chips.bet > chips.total:
                print("Sorry. You cannot bet more that what you have")
            else:
                break