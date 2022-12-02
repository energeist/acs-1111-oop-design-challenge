from cards import Deck
from cards import Hand

class Person:
    def __init__(self, person_name, chips = 0):
        self.person_type = "bystander"
        self.chips = chips
        self.person_name = person_name
        self.hand = "bystanders don't hold any cards!"

    def _introduce_self(self):
        print(f"Hi, I'm {self.person_name}!")

    def _hit_or_stand(self): 
        print("I'm just STANDING around!")

class Player(Person):
    def __init__(self, person_name, chips = 1000):
        self.person_type = 'player'
        self.person_name = person_name
        self.chips = chips
        self.hand = Hand()
        self.wins = 0
        self.ties = 0
        self.losses = 0    

    def _introduce_self(self):
        super(Player, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.")

    def _hit_or_stand(self): 
        player_input = ("Would you like to (H)it or (S)tand?")
        while True: 
            if player_input.lower() == "h":
                print(f"{self.name} hits!")        
            elif player_input.lower == "s":
                print(f"{self.name} will stand.")
            else:
                print("Sorry, please input 'h' for hit or 's' for stay")
        return player_input    

class Dealer(Person):
    def __init__(self, person_name):
        self.person_name = person_name
        self.person_type = 'dealer'
        self._deck = Deck()
        self.hand = Hand()
    
    def _introduce_self(self):
        super(Dealer, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.")
        print(f"Don't forget, the house always wins!")

    def deal_starting_hands(self, player_list):
        self._deck._shuffle()
        deal_round = 0
        while deal_round < 2:
            for player in player_list:
                incoming_card = self._deck.deal()
                incoming_card.is_hidden = False
                player.hand.add_card(incoming_card)
            incoming_card = self._deck.deal()
            if deal_round == 1:
                incoming_card.is_hidden = False
            self.hand.add_card(incoming_card)    
            deal_round += 1

    def _hit_or_stand(self): 
        # use score calc method and logic, this follows a structure
        # score >= 17 always stand
        # score < 17 always hit
        pass

#TEST CODE

def test():
    test_person = Person('Test')
    test_person._introduce_self()
    print(test_person.person_type)
    print(test_person.hand)
    print()
    mark = Player('Mark')
    mark._introduce_self()
    mark.hand.deal_hand()
    mark.hand.show_hand()
    print(f"Score for this hand: {mark.hand.calc_score()}")
    print()
    shar = Player('Sharmaine')
    shar._introduce_self()
    shar.hand.deal_hand()
    shar.hand.show_hand()
    print(f"Score for this hand: {shar.hand.calc_score()}")
    print()
    dealer = Dealer('Dealy McDealerface')
    dealer._introduce_self()
    dealer.hand.deal_hand()
    dealer.hand.show_hand()
    print(f"Score for this hand: {dealer.hand.calc_score()}")
    print()
    dealer._Dealer__deck._shuffle()
    dealer._Dealer__deck._show_deck()
    print()

# test()