from cards import Deck
from cards import Hand

class Players():
    def __init__(self, chips, name):
        self.name = name
        self.hand = []
        self.chips = chips
        self.wins = 0
        self.losses = 0

    def hit(deck, hand):
        hand.add_card(deck.deal())
        hand.adjust_for_ace()

    def hit_or_pass(deck): 
        player_input = ("Would you like to (H)it or (P)ass?")

        while True: 
            if player_input.lower() == "h":
                print("Player hits")
        
            elif player_input.lower == "s":
                print("Player passes turn")
            else:
                print("Sorry, please input h for hit or p for pass")
            return player_input
    
    

class Dealer(Players):
    def __init__(self, deck):
        self.deck = deck
    
    def check_for_ace(self, hand):
        for card in hand:
            if card.values == "Ace":
                return True
            else:
                return False


#TEST CODE
mark = Players()
mark.hit_or_pass()

shar = Players()
shar.hit_or_pass()
