from cards import Deck
from cards import Hand
from abc import ABC, abstractmethod 

"""
Person class is called to instantiate new people that's composed of Players, Dealer, and spectator?
    Input parameters - none
        - person_type that's been defined
        - chips - int - starting at 0
        - person_name - str - spectator's name
        - hand - str- that's been defined
    Output - none until methods are called
"""
class Person(ABC):
    def __init__(self, person_name, chips = 0):
        """
        Class Initialization
        """
        self.person_type = "spectator"
        self.chips = chips
        self.person_name = person_name
        self.hand = "Spectators don't hold any cards!"


    @abstractmethod
    def _introduce_self(self):
        """
        _introduce_self is a private method that states the person_name in the game. Made private
        because only Person can have access to this method.
        Inputs: none
        Return: none
        """
        print(f"Hi, I'm {self.person_name}!")
        pass

    @abstractmethod
    def _hit_or_stand(self): 
        """
        _hit_or_stands is a private method that states what the spectator is doing in the game. Made private
        because only Person can have access to this method.
        Inputs: none
        Return: none
        """
        print("I'm just standing around!")
        pass

class CasinoEmployee: ## for Mixin on Dealer class 
    """
    CasinoEmployee class is called for Mixin on Dealer class 
    """
    @staticmethod
    def _warn_players():
        """
        _warn_players is a private method that states a warning if someone is suspected of cheating! Made private
        because only the Dealer can have access to this method.
        Inputs: none
        Return: none
        """
        print("If I catch you counting cards then I'll call the pit boss!")
    
    @staticmethod
    def _call_pit_boss():
        """
        _call_pit_boss is a private method that calls someone out for cheating! Made private
        because only the Dealer can have access to this method.
        Inputs: none
        Return: none
        """
        print("You're obviously cheating! I'm calling the pit boss!")

class Player(Person):
    """
    Player class is called to instantiate new Person objects for the dealer.
    Input params - person_type - str - defaults to player
        - person_name - str - player's name
        - chips - int - set at 100
        - hand - object of Hand class
        - is_still_playing - boolean - set to True
        - is_stille_choosing - boolean - set to True
        - wins - int - starts at 0
        - ties - int - starts at 0
        - losses - int - starts at 0
    Output - none until methods are called
    """
    def __init__(self, person_name, chips = 100):
        """
        Class Initialization
        """
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
        """
        _introduce_self is a private method that states the person_type in the game. Made private
        because only he player needs access to this method.  
        Inputs: none
        Return: none
        """
        super(Player, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.\n")


    def _hit_or_stand(self, player):
        """
        _hit_or_stand is a private method states whether the player hits or stands. Made private because only the
        player needs access to this method. 
        Inputs: player_input = asks whoever is the player whether they would like to hit or stand
        Return: none
        """
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
    """
    Dealer class is called to instantiate new Person objects for CasinoEmployee.
    Input params - person_type - str - defaults to dealer
        - person_name - str - dealer's name
        - _deck - object of Deck class
        - hand - object of Hand class
        - is_stille_choosing - boolean - set to True
        - is_still_bust - boolean - set to False
    Output - none until methods are called
    """
    def __init__(self, person_name):
        """
        Class Initialization
        """
        self.person_name = person_name
        self.person_type = "dealer"
        self._deck = Deck()
        self.hand = Hand()
        self.is_still_choosing = True
        self.is_bust = False
    
    def _introduce_self(self):
        """
        _introduce_self is a private method that states the person_type in the game. Made private because only the dealer
        can access this method.
        Inputs: none
        Return: none
        """
        super(Dealer, self)._introduce_self()
        print(f"I'm a {self.person_type} in this game.")
        print(f"Don't forget, the house always wins!\n")

    def deal_starting_hands(self, player_list):
        """
        deal_starting_hands is a method that  
        Inputs: none
        Return: none
        """
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
        """
        _hit_or_stand is a private method that checks if the cards in player's hand is greater than
        17. Made private because only the Dealer can call this method.
        Inputs: none
        Return: none
        """

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