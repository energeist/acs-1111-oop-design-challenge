from cards import Deck
from cards import Hand
from abc import ABC, abstractmethod
import re 

class Person(ABC):
    def __init__(self, person_name, chips = 0):
        self._person_type = "spectator"
        self.__chips = chips
        self._person_name = person_name
        self._hand = "Spectators don't hold any cards!"

    @abstractmethod
    def _introduce_self(self):
        print(f"Hi, I'm {self._person_name}!")
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
    def __init__(self, person_name, starting_chips = 100):
        self._person_type = "player"
        self._person_name = person_name
        self.__chips = starting_chips
        self._hand = Hand()
        self._current_bet = 0
        self._is_still_playing = True
        self._is_still_choosing = True
        self._is_bust = False
        self._wins = 0
        self._ties = 0
        self._losses = 0    

    def _introduce_self(self):
        super(Player, self)._introduce_self()
        print(f"I'm a {self._person_type} in this game.\n")

    def _hit_or_stand(self):
        player_input = '' 
        while player_input.strip().lower() not in ['h','s']:
            player_input = input(f"{self._person_name} - would you like to (H)it or (S)tand? > ").strip().lower()
            if player_input == "h":
                print(f"{self._person_name} hits!\n")        
            elif player_input == "s":
                print(f"{self._person_name} will stand.\n")
                self._is_still_choosing = False
            else:
                print("Sorry, please input 'h' for hit or 's' for stand\n")

    def __make_bet(self):
        """
        __make_bet method allows the current player to make a bet
        Made private because players make their own bets
        Inputs: none
        Return: none
        """
        is_valid_bet = False
        print(f"How much would you like to bet, {self._person_name}?")   
        while not is_valid_bet:
            current_bet = input(f"Minimum bet is 10, maximum bet is {self.__chips}, or enter 'x' to leave the table. > ")
            while not re.match("[0-9xX]", current_bet):
                current_bet = input(f"Invalid bet, {self._person_name}! Minimum bet is 10, maximum bet is {self.__chips}, or enter 'x' to leave the table. > ")            
            if current_bet.strip().lower() == 'x':
                self._is_still_playing = False
                print(f"Thanks for playing, {self._person_name}!")
                current_bet = 0
                return False
            elif int(current_bet) >= 10 and int(current_bet) <= self.__chips:
                is_valid_bet = True
                self._current_bet = int(current_bet)
                self.__change_chips(-(int(current_bet)))
                return True
            else:
                print(f"Invalid bet, {self._person_name}!")

    def __change_chips(self, amount):
        """
        __change_chips method changes the current player's chips total
        Made private because only players can change their own chip total.  They remove chips from their stash when making a bet and add chips on a tie or win.
        Inputs: amount - int - amount of chips to add or subtract (-ve amount)
        Return: none
        """
        self.__chips += amount

class Dealer(Person, CasinoEmployee): # Multiple inheritance / Mixin
    def __init__(self, person_name):
        self._person_type = "dealer"
        self._person_name = person_name
        self._deck = Deck()
        self._hand = Hand()
        self._is_still_choosing = True
        self._is_bust = False
    
    def _introduce_self(self):
        super(Dealer, self)._introduce_self()
        print(f"I'm a {self._person_type} in this game.")
        print(f"Don't forget, the house always wins!\n")

    def __deal_starting_hands(self, player_list):
        deal_round = 0
        while deal_round < 2:
            for player in player_list:
                incoming_card = self._deck._deal()
                incoming_card.is_hidden = False
                player._hand._add_card(incoming_card)
            incoming_card = self._deck._deal()
            if deal_round == 1:
                incoming_card._is_hidden = True
            self._hand._add_card(incoming_card)    
            deal_round += 1

    def _hit_or_stand(self):
        if self._hand._Hand__calc_score() >= 17:
            self._is_still_choosing = False
        else:
            self._is_still_choosing = True
