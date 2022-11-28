import random

class Cards:
    def __init__(self, value, suit, deck):
        self.value = value
        self.suit = suit
        self.deck = deck

class Deck:
    def __init__(self, deck_of_cards):
        self.deck_of_cards = deck_of_cards
        self.create_deck()

    values = {
            '1':'Ace',
            '2':'2',
            '3':'3',
            '4':'4',
            '5':'5',
            '6':'6',
            '7':'7',
            '8':'8',
            '9':'9',
            '10':'10',
            '11':'Jack',
            '12':'Queen',
            '13':'King'
        }

    suits = {   
            'spades': {
                'color':'black',
                'symbol':'♠️'
            },
            'clubs': {
                'color':'black',
                'symbol':'♣️'
            },
            'diamonds': {
                'color':'red',
                'symbol':'♦️'
            },
            'hearts': {
                'color':'red',
                'symbol':'♥️'
            }
        }
        
    def create_deck(self):
        for suit in self.suits:
            for value in self.values:
                print(self.suits[suit]['color'], " ", self.suits[suit]['symbol'])
                print(value, " ", self.values[value])
                self.deck_of_cards.append(Cards(value, suit, self))

    def show_deck(self):
        print(len(self.deck_of_cards))
        for card in self.deck_of_cards:
            print(card.__dict__)

    def shuffle(self):
        random.shuffle(self.deck_of_cards)
        return self.deck_of_cards
        
my_deck = Deck([])
my_deck.show_deck()
my_deck.shuffle()
my_deck.show_deck()

# class Hand:
