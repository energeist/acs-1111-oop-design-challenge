import random

class Cards:
    def __init__(self, value, card_name, suit, symbol, color, deck):
        self.value = value
        self.card_name = card_name
        self.suit = suit
        self.symbol = symbol
        self.color = color
        self.deck = deck
        self.is_hidden = False

    def __dict__(self):
        if self.color == 'red':
            color_mod = '\33[31m'
        else:
            color_mod = ''
        return(f'[{self.card_name} {color_mod}{self.symbol} {self.suit}\33[0m]')

class Deck:
    def __init__(self):
        self.deck_of_cards = []
        self.__create_deck()

    values = { # hold positional values in case of sorting
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
        
    def __create_deck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck_of_cards.append(
                    Cards(int(value), self.values[value], suit, self.suits[suit]['symbol'], self.suits[suit]['color'], self))

    def _show_deck(self):
        print(f"There are {len(self.deck_of_cards)} cards left in this deck")
        for card in self.deck_of_cards:
            print(card.__dict__())

    def _shuffle(self):
        random.shuffle(self.deck_of_cards)
        return self.deck_of_cards

    def deal(self):
        if len(self.deck_of_cards) > 1:
            return self.deck_of_cards.pop()
        else:
            print("There are no more cards in the deck!")
        

class Hand(Deck):
    def __init__(self, starting_cards = 2):
        self.starting_cards = starting_cards
        self.cards = []
        self.hand_value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calc_score(self):
        card_score = 0
        self.hand_value = 0 # initialize to 0
        aces = []
        for card in self.cards:
            if card.is_hidden:
                card_score = 0 # do not show card value for face down cards
            else:
                if card.card_name in ['Jack','Queen','King']:
                    card_score = 10
                elif card.card_name == 'Ace':
                    aces.append(card)
                    card_score = 0 # keep score at zero until counting aces in the list after the other cards
                else:
                    card_score = int(card.card_name)       
                self.hand_value += card_score
        for ace in aces:
            if self.hand_value > 10:
                card_score = 1
            else:
                card_score = 11
            self.hand_value += card_score
        return self.hand_value
    
    def show_hand(self):
        for card in self.cards:
            if card.is_hidden:
                print("[FACE DOWN CARD]")
            else:
                print(card.__dict__())

    def discard_hand(self, table):
        for card in self.cards:
            table.discard_pile.append(card)
            self.cards = []
        
#TEST CODE
# my_deck = Deck()
# my_deck._shuffle()
# my_deck._show_deck()

# hand.deal_hand()
# hand.show_hand()
# print(hand.calc_score())