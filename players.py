# so rough, haha sorry mark (:
# will add to it in a bit!

class Person:
    def __init__(self, name, player, dealer, wallet):
        self.name = name
        self.player = player
        self.dealer = dealer
        self.wallet = wallet

    def greet(self):
        print(f"Hello, {self.name} Welcome!")

class Player(Person):
    def __init__(self):
        self.hand = []
        self.wallet = 0
        self.wins = 0
        self.losses = 0

    def bet(self, wallet):
        self.wallet = wallet

    # def add_card(self):
    #     pass


    def hit_or_pass():
        while True:
            action = input("Would you like to hit(h) or pass(p)?")
            if action.lower() == "h":
                return True
            elif action.lower() == "p":
                return False

class Dealer(Person):
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def greet_player(self):
        print(f"Hello {self.player} I'm {self.dealer}")

    def draw(self, deck):
        card = deck.draw()
        self.hand.append(card)
    