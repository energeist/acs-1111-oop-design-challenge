from cards import Deck
from cards import Hand
from players import Person
from players import Player
from players import Dealer
from datetime import datetime
from decorators import phase_announcement
import re

class Table:
    """
    Deck class is called to instantiate new Deck objects that are composed of Cards objects.
    Input params - none
        - Initializes with player_list as an empty list
        - Initializes with a predefined Dealer object
        - Initializes with private create_players method to take user input on instantiation
        - Initializes with discard_pile as an empty list 
    Output - none until methods are called
    """
    def __init__(self):
        """
        Class intialization
        """
        self.player_list = []
        self.dealer = Dealer("Dealy McDealerface")
        self._Table__create_players()
        self.discard_pile = []

    def __create_players(self):
        """
        __create_players method builds a deck of Cards by appending Cards objects to the deck_of_cards list.
        Made private because only the Table the game can only start with new players at a Table 
        Inputs: none
        Return: none
        """
        self.all_people = []
        print("This game will allow for a maximum of 3 players.")
        print("The dealer hits on 16 and stands on 17 or higher.  Winning pays out 2:1.\n")
        player_count = 0
        while player_count < 3:
            player_name = ''
            more_players = True
            while not player_name:
                player_name = input(f"Please input a player name: > ")
            player_count += 1
            self.player_list.append(Player(player_name))
            if player_count < 3:
                another_player = ''
                while another_player.strip().lower() not in ['y','n']:
                    another_player = input(f'Would you like register another player? Please enter y or n > ')
                if another_player.strip().lower() == 'n':
                    break
        for player in self.player_list:
            self.all_people.append(player)
        self.all_people.append(self.dealer) # dealer appended last because they go last in play order    

    def play_hand(self, player):
        """
        play_hand method is a game logic sequence that plays the current Player's hand
        Inputs: player - Player object - current Player making choices to play
        Return: none
        """
        while player._is_still_choosing:
            if player._person_type == 'dealer':
                for card in player._hand.cards:
                    if card._is_hidden:
                        card._is_hidden = False
                        print(f"{player._person_name} flips over their hidden card and reveals their starting hand.")
                        player._hand._show_hand()
                        print(f"{player._person_name}'s hand is worth {player._hand._Hand__calc_score()} points.\n")
                print()
                player._hit_or_stand()
            else:
                player._hit_or_stand()
                # if player.is_still_choosing == True then player selected (H)it. 
            if player._is_still_choosing:
                incoming_card = self.dealer._deck._deal()
                if not incoming_card: # no cards left in deck, returned False => append discarded cards to deck list and shuffle.  Not used right now because deck should reshuffle before we get to this point.
                    for card in table.discard_pile:
                        table.dealer._deck._deck_of_cards.append(card)
                    table.dealer._deck._shuffle()
                    incoming_card = self.dealer._deck._deal()
                else:    
                    print(f"{player._person_name} is dealt {incoming_card.__dict__()}")
                    player._hand._add_card(incoming_card)
                    player._hand._show_hand()
                    print(f"{player._person_name}'s hand is worth {player._hand._Hand__calc_score()} points.\n")
            else:
                player._is_still_choosing = True # resetting for next round
                break
            if player._hand._Hand__calc_score() > 21:
                print(f"{player._person_name} has more than 21 points and they've busted!\n")
                player._is_bust = True
                if player._person_type == 'player':
                    player._losses += 1
                break

    def show_all_hands(self):
        """
        show_all_hands method is a game logic sequence that displays the hands for all Players and the Dealer at the table
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if not player._is_bust and player._is_still_playing: 
                print(f"Cards in {player._person_name}'s hand:")
                player._hand._show_hand()
                print(f"{player._person_name}'s hand is worth {player._hand._Hand__calc_score()} points.\n")
        print(f"Cards in {self.dealer._person_name}'s hand:")
        self.dealer._hand._show_hand()
        print(f"{self.dealer._person_name}'s hand is worth {self.dealer._hand._Hand__calc_score()} points.\n")

    @phase_announcement('introduction')
    def introduce_players(self):
        """
        introduce_players method is a game logic sequence that introduces the Players and Dealer by calling their internal methods
        Inputs: none
        Return: none
        """
        print(f"There are {len(table.player_list)} players and a dealer at the table.\n")
        for person in self.all_people:
            person._introduce_self()
        self.dealer._warn_players()

    @phase_announcement('betting')
    def get_player_bets(self):
        """
        get_player_bets method is a game logic sequence that gets bet input from each Player still in the game.  If a player chooses to leave the table then they will also discard their hand.
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if player._Player__chips < 10:
                print(f"Sorry {player._person_name}, looks like you don't have enough chips to keep playing!")
                player._is_still_playing = False
            if player._is_still_playing:
                if not player._Player__make_bet():
                    player._hand._discard_hand(self)

                print()

    def player_check(self):
        """
        player_check method is a game logic sequence that checks to see if there are still Players in the game
        Inputs: none
        Return: players_playing - int - number of Players with is_stil_playing attribute set to True
        """
        players_playing = 0
        for player in self.player_list:
            if player._is_still_playing:
                player._is_bust = False
                players_playing += 1
        table.dealer._is_bust = False
        return players_playing

    @phase_announcement('play')
    def play_round(self):
        """
        play_round method is a game logic sequence that determines whether the Dealer's hand needs to be played or not
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if player._is_still_playing:
                print(f"It's {player._person_name}'s turn to play their hand.")
                player._hand._show_hand()
                print(f"{player._person_name}'s hand is worth {player._hand._Hand__calc_score()} points.\n")
                self.play_hand(player)

        all_bust = True
        for player in self.player_list:
            if not player._is_bust:
                all_bust = False

        if not all_bust:
            # play dealer hand
            self.play_hand(self.dealer)

    @phase_announcement('scoring')
    def round_scoring(self):
        """
        round_scoring method is a game logic sequence that calculates the scores for each hand and determines win/loss status, pays or removes chips and discards all hands to the discard_pile
        Inputs: none
        Return: none
        """
        if self.dealer._is_bust:
            print("The dealer is bust! All remaining players win!\n")
            for player in self.player_list:
                if not player._is_bust:
                    player._wins += 1
                    player._Player__change_chips(player._current_bet * 2)
                    player._current_bet = 0
                player._hand._discard_hand(table)
        else:
            dealer_score = self.dealer._hand._Hand__calc_score()
            for player in self.player_list:
                if player._is_still_playing:
                    if player._is_bust:
                        print(f"{player._person_name} went bust!\n")
                    else:
                        player_score = player._hand._Hand__calc_score()
                        if player_score > dealer_score:
                            player._wins += 1
                            print(f"{player._person_name}'s hand is {player_score} points, which beats the dealer's {dealer_score} points! {player._person_name} wins!\n")
                            player._Player__change_chips(player._current_bet * 2)
                            player._current_bet = 0
                            if player._Player__chips >= 1000:
                                self.dealer._call_pit_boss()
                                print(f"The pit boss caught {player._person_name} counting cards and removed them from the game!")
                                player._is_still_playing = False
                        elif player_score == dealer_score:
                            player._ties += 1
                            print(f"{player._person_name} ties with the dealer!\n")
                            player._Player__change_chips(player._current_bet)
                            player._current_bet = 0
                        else:
                            player._losses += 1
                            player._current_bet = 0
                            print(f"The dealer's hand is {dealer_score} points, which beats {player._person_name}'s {player_score} points. {player._person_name} loses!\n")
                player._hand._discard_hand(self)
        table.dealer._hand._discard_hand(self)
    
    def reshuffle_discard_pile(self):
        """
        reshuffle_discard_pile method is a game logic sequence that moves cards from the discard_pile back to the deck and reshuffles as necessary
        Inputs: none
        Return: none
        """
        if len(table.discard_pile) <= 30:
            print(f"There are {len(table.discard_pile)} cards in the discard pile\n")
        else:
            print("Reshuffling the discard pile back in to the deck...\n")
            for card in table.discard_pile:
                table.dealer._deck._deck_of_cards.append(card)
            table.dealer._deck._shuffle()
            table.discard_pile = []
            print(f"There are now {len(table.dealer._deck._deck_of_cards)} cards in the deck.\n")

## GAME RUN CODE

if __name__ == "__main__":
    # init with player creation
    
    try: # Demo ABC on Person
        person = Person('Test')
    except TypeError:
        print("Can't instantiate the abstract Person class!\n")
    
    table = Table()

    #shuffle deck
    table.dealer._deck._shuffle()
    rounds = 0

    table.introduce_players()

    # loop while there are still players in the game
    players_playing = 1
    while players_playing > 0:

        # check for players at the table
        players_playing = table.player_check()
        
        # get post-deal bets
        table.get_player_bets()

        # check for players at the table
        players_playing = table.player_check()

        if players_playing > 0:
            rounds += 1
            print(f"Start of ROUND {rounds}!\n")

            # deal starting hands
            table.dealer._Dealer__deal_starting_hands(table.player_list)

            # show starting hands
            table.show_all_hands()

            # play each player hand still in game
            table.play_round()

            # compare scores and generate W/T/L against dealer, pay out chips, discard all hands to discard pile
            table.round_scoring()

            # reshuffle discard pile back in to deck if needed
            table.reshuffle_discard_pile()

        # check for players again and reset variables
        players_playing = table.player_check()

    if rounds > 0 :
        print(f"All players are out of chips or they've left the table. After {rounds} rounds, the game is over!\n")
        print("End of game summary:")
        for player in table.player_list:
            print(f"{player._person_name} ended the game with {player._Player__chips} chips.  They had {player._wins} wins, {player._ties} ties and {player._losses} losses.")
    else:
        print("Everyone left before the game could even start!")