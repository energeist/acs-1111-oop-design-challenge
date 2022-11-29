from cards import Cards
from cards import Deck
import random

class Person:
    def __init__(self,name):
        self.name = name
        self.hand = []

    def greet_person(self):
        print(f"Hi, {self.name} ") # will add to it 


    def sort(self, cards):
        self.cards = cards

    def remove_card(self):
        pass

    def show_cards(self):
        for card in self.cards:
            print(card)