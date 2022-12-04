import random

class Cards:
    """
    Cards class is called to instantiate new Card objects that initialize with an order value,
    a card name, suit, symbol, color and deck association.
    Input params: 
        - value - int - order (index) value of card within a suit
        - card_name - str - common name of card value e.g. Ace / 2..9 / Jack, Queen, King
        - suit - str - suit belonging to the card (hearts, etc.)
        - symbol - str - symbol associated with the suit
        - color - str - color associated with the suit
        - deck - object - deck object instance associated with the card.
    Output - none until methods are called
    """
    def __init__(self, value, card_name, suit, symbol, color, deck):
        """
        Class initialization
        All attributes (except _is_hidden) made private because each instance of a Cards object has its own unique attribute values on instantiation, and they can never change.
        _is_hidden made protected because the dealer can change this attribute from True to False.
        """
        self.__value = value
        self.__card_name = card_name
        self.__suit = suit
        self.__symbol = symbol
        self.__color = color
        self.__deck = deck
        self._is_hidden = False

    def __dict__(self): #override dict magic method for readable string output
        """
        __dict__ magic method override to produce friendly string output
        Inputs: none
        Return: string containing readable card description
        """
        if self.__color == 'red':
            color_mod = '\33[31m'
        else:
            color_mod = ''
        return(f'[{self._Cards__card_name} {color_mod}{self.__symbol} {self.__suit}\33[0m]')

class Deck:
    """
    Deck class is called to instantiate new Deck objects that are composed of Cards objects.
    Input params - none
        - Initializes with protected _deck_of_cards as an empty list, only objects with a Deck need to manipulate this attribute
        - Initializes by calling the private create_deck method which build a deck of 52 card objects inside the previously empty deck_of_cards list
    Output - none until methods are called
    """
    def __init__(self):
        """
        Class initialization
        __create_deck made private because this is only accessed by the Deck on instantiation
        """
        self._deck_of_cards = []
        self.__create_deck()

    # class attribute dictionaries for card building
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
        """
        __create_deck method builds a deck of Cards by appending Cards objects to the deck_of_cards list.
        Made private because only the Deck class should be able to access this method
        Inputs: none
        Return: none
        """
        for suit in self.suits:
            for value in self.values:
                self._deck_of_cards.append(
                    Cards(int(value), self.values[value], suit, self.suits[suit]['symbol'], self.suits[suit]['color'], self))

    def _show_deck(self):
        """
        _show_deck method prints the entire deck of cards.
        Made protected because only objects with a deck need to show the deck of cards
        Inputs: none
        Return: none
        """
        print(f"There are {len(self._deck_of_cards)} cards left in this deck\n")
        for card in self._deck_of_cards:
            print(card.__dict__())

    def _shuffle(self):
        """
        _shuffle method uses random.shuffle to shuffle the deck of cards
        Made protected because only objects with a deck need to shuffle the deck of cards
        Inputs: none
        Return: shuffled deck of cards
        """
        random.shuffle(self._deck_of_cards)
        return self._deck_of_cards

    def _deal(self):
        """
        deal method removes and returns the last card (index -1) from the deck (which we refer to as the top of the deck)
        Made protected because only objects with a deck should be able to deal cards
        Inputs: none
        Return: Last card from the deck list (Truthy value) or False, if there are no cards left in the deck
        """
        if len(self._deck_of_cards) > 1:
            return self._deck_of_cards.pop()
        else:
            print("There are no more cards in the deck!\n")
            return False
        
class Hand:
    """
    Hand class is called to instantiate new Hand objects for the dealer and each player at the table.
    Input params - starting_cards - int - defaults to '2' for Blackjack
        - cards - blank list on class initialization used to hold Cards that are dealt to the Hand
        - hand_value - int - object-associated tracker for current hand value
    Output - none until methods are called
    """
    def __init__(self, starting_cards = 2):
        """
        Class initialization
        """
        self.starting_cards = starting_cards
        self.cards = []
        self.hand_value = 0

    def _add_card(self, card):
        """
        add_card method appends a Card to the Hand's cards list.
        Made protected because any object with a hand should be able to add a dealt card to their hand
        Inputs: card - a Cards object
        Return: none
        """
        self.cards.append(card)

    def __calc_score(self):
        """
        calc_score method calculates the current Hand's score and updates self.hand_value.
        Made private because only the value of the cards in the hand can contribute to the hand's score.
        Inputs: none
        Return: self.hand_value
        """
        card_score = 0
        self.hand_value = 0 # initialize to 0
        aces = []
        for card in self.cards:
            if card._is_hidden:
                card_score = 0 # do not show card value for face down cards
            else:
                if card._Cards__card_name in ['Jack','Queen','King']:
                    card_score = 10
                elif card._Cards__card_name == 'Ace':
                    aces.append(card)
                    card_score = 0 # keep score at zero until counting aces in the list after the other cards
                else:
                    card_score = int(card._Cards__card_name)       
                self.hand_value += card_score
        for ace in aces:
            if self.hand_value > 10:
                card_score = 1
            else:
                card_score = 11
            self.hand_value += card_score
        return self.hand_value
    
    def _show_hand(self):
        """
        show_hand loops through the cards in the current Hand and shows them, or shows [FACE DOWN CARD] if the Cards is_hidden attribute is set to True.
        Inputs: none
        Return: none
        """
        for card in self.cards:
            if card._is_hidden:
                print("[FACE DOWN CARD]")
            else:
                print(card.__dict__())

    def _discard_hand(self, table):
        """
        discard_hand appends each card in the Hand to the Table's discard pile, and then resets the Hand's cards list to a blank list.
        Made protected because any object with a hand should be able to discard their own hand
        Inputs: none
        Return: none
        """
        for card in self.cards:
            table.discard_pile.append(card)
            self.cards = []