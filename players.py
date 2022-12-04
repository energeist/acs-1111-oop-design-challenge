from cards import Deck
from cards import Hand
from abc import ABC, abstractmethod 

class Person(ABC):
    def __init__(self, person_name, chips = 0):
        self.person_type = "spectator"
        self.chips = chips
        self.person_name = person_name
        self.hand = "Spectators don't hold any cards!"

    @abstractmethod
    def _introduce_self(self):
        print(f"Hi, I'm {self.person_name}!")
        pass

    @abstractmethod
    def _hit_or_stand(self): 
        print("I'm just standing around!")
        pass

class CasinoEmployee: ## for Mixin on Dealer class 
    
    @staticmethod
    def _warn_players():
        print("If I catch you counting cards then I'll call the pit boss!")
    
    @staticmethod
    def _call_pit_boss():
        print("You're obviously cheating! I'm calling the pit boss!")

class Player(Person):
    def __init__(self, person_name, chips = 100):
        self.person_type = "player"
        self.person_name = person_name
        self.chips = chips
        self.hand = Hand()
        self.is_still_playing = True
        self.is_still_choosing = True
        self.is_bust = False
        self.wins = 0
        self.ties = 0
        self.losses = 0    

    def _introduce_self(self):
        super(Player, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.\n")

    def _hit_or_stand(self, player):
        player_input = '' 
        while player_input.strip().lower() not in ['h','s']:
            player_input = input(f"{player.person_name} - would you like to (H)it or (S)tand? > ").strip().lower()
            if player_input == "h":
                print(f"{self.person_name} hits!\n")        
            elif player_input == "s":
                print(f"{self.person_name} will stand.\n")
                player.is_still_choosing = False
            else:
                print("Sorry, please input 'h' for hit or 's' for stand\n")  

class Dealer(Person, CasinoEmployee): # Multiple inheritance / Mixin
    def __init__(self, person_name):
        self.person_name = person_name
        self.person_type = "dealer"
        self._deck = Deck()
        self.hand = Hand()
        self.is_still_choosing = True
        self.is_bust = False
    
    def _introduce_self(self):
        super(Dealer, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.")
        print(f"Don't forget, the house always wins!\n")

    def deal_starting_hands(self, player_list):
        deal_round = 0
        while deal_round < 2:
            for player in player_list:
                incoming_card = self._deck.deal()
                incoming_card.is_hidden = False
                player.hand.add_card(incoming_card)
            incoming_card = self._deck.deal()
            if deal_round == 1:
                incoming_card.is_hidden = True
            self.hand.add_card(incoming_card)    
            deal_round += 1

    def _hit_or_stand(self):

        # print(f"Cards in {self.person_name}'s hand:")
        # self.hand.show_hand()
        # print(f"{self.person_name}'s hand is worth {self.hand.calc_score()} points.\n")
        if self.hand.calc_score() >= 17:
            self.is_still_choosing = False
        else:
            self.is_still_choosing = True


#TEST CODE

def test():
    mark = Player('Mark')
    mark._introduce_self()
    print()
    shar = Player('Sharmaine')
    shar._introduce_self()
    print()
    dealer = Dealer('Dealy McDealerface')
    dealer._introduce_self()
    print()
    # test_person = Person('Test')
    # test_person._introduce_self()
    # print(test_person.person_type)
    # print(test_person.hand)
    # print()

# test()