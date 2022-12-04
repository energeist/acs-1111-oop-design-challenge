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
 
    def get_bet(self, player):
        """
        get_bet method takes and validates bet input from a user, then stores that bet in the current Player object's current_bet attribute
        Inputs: none
        Return: none
        """
        is_valid_bet = False
        player.current_bet = ''
        if player.chips < 10:
            print(f"Looks like you've had a rough night, {player.person_name}! You don't have enough chips to play.")
            player.is_still_playing = False
            player.is_bust = True
        else:
            print(f"How much would you like to bet, {player.person_name}?")   
            while not is_valid_bet:
                player.current_bet = input(f"Minimum bet is 10, maximum bet is {player.chips}, or enter 'x' to leave the table. > ")
                while not re.match("[0-9xX]", player.current_bet):
                    player.current_bet = input(f"Invalid bet, {player.person_name}! Minimum bet is 10, maximum bet is {player.chips}, or enter 'x' to leave the table. > ")            
                if player.current_bet.strip().lower() == 'x':
                    player.is_still_playing = False
                    print(f"Thanks for playing, {player.person_name}!")
                    player.hand.discard_hand(self)
                    self.all_people.remove(player)
                    player.current_bet = 0
                    break
                elif int(player.current_bet) >= 10 and int(player.current_bet) <= player.chips:
                    is_valid_bet = True
                else:
                    print(f"Invalid bet, {player.person_name}!")

    def play_hand(self, player):
        """
        play_hand method is a game logic sequence that plays the current Player's hand
        Inputs: player - Player object - current Player making choices to play
        Return: none
        """
        while player.is_still_choosing:
            if player.person_type == 'dealer':
                for card in player.hand.cards:
                    if card.is_hidden:
                        print(f"{player.person_name} flips over their hidden card.\n")
                    card.is_hidden = False
                player.hand.show_hand()
                print()
                player._hit_or_stand()
            else:
                player._hit_or_stand(player)
            if player.is_still_choosing:
                incoming_card = self.dealer._deck.deal()
                if not incoming_card: # no cards left in deck, returned False => append discarded cards to deck list and shuffle
                    for card in table.discard_pile:
                        table.dealer._deck.deck_of_cards.append(card)
                    table.dealer._deck._shuffle()
                else:    
                    print(f"{player.person_name} is dealt {incoming_card.__dict__()}")
                    player.hand.add_card(incoming_card)
                    player.hand.show_hand()
                    print(f"{player.person_name}'s hand is worth {player.hand.calc_score()} points.\n")
            else:
                player.is_still_choosing = True # resetting for next round
                break
            if player.hand.calc_score() > 21:
                print(f"{player.person_name} has more than 21 and they've busted!\n")
                player.is_bust = True
                if player.person_type == 'player':
                    player.losses += 1
                    player.chips -= int(player.current_bet)
                break

    def show_all_hands(self):
        """
        show_all_hands method is a game logic sequence that displays the hands for all Players and the Dealer at the table
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if not player.is_bust and player.is_still_playing: 
                print(f"Cards in {player.person_name}'s hand:")
                player.hand.show_hand()
                print(f"{player.person_name}'s hand is worth {player.hand.calc_score()} points.\n")
        print(f"Cards in {self.dealer.person_name}'s hand:")
        self.dealer.hand.show_hand()
        print(f"{self.dealer.person_name}'s hand is worth {self.dealer.hand.calc_score()} points.\n")

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
        get_player_bets method is a game logic sequence that gets bet input from each Player still in the game
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if player.is_still_playing:
                self.get_bet(player)
                print()

    def player_check(self):
        """
        player_check method is a game logic sequence that checks to see if there are still Players in the game
        Inputs: none
        Return: players_playing - int - number of Players with is_stil_playing attribute set to True
        """
        players_playing = 0
        for player in self.player_list:
            if player.is_still_playing:
                player.is_bust = False
                players_playing += 1
        table.dealer.is_bust = False
        return players_playing

    @phase_announcement('play')
    def play_round(self):
        """
        play_round method is a game logic sequence that determines whether the Dealer's hand needs to be played or not
        Inputs: none
        Return: none
        """
        for player in self.player_list:
            if player.is_still_playing:
                print(f"It's {player.person_name}'s turn to play their hand.")
                player.hand.show_hand()
                print(f"{player.person_name}'s hand is worth {player.hand.calc_score()} points.\n")
                self.play_hand(player)

        all_bust = True
        for player in self.player_list:
            if not player.is_bust:
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
        if self.dealer.is_bust:
            print("The dealer is bust! All remaining players win!\n")
            for player in self.player_list:
                if not player.is_bust:
                    player.wins += 1
                    player.chips += int(player.current_bet)
                player.hand.discard_hand(table)
        else:
            dealer_score = self.dealer.hand.calc_score()
            for player in self.player_list:
                if player.is_still_playing:
                    if player.is_bust:
                        print(f"{player.person_name} went bust!\n")
                    else:
                        player_score = player.hand.calc_score()
                        if player_score > dealer_score:
                            player.wins += 1
                            print(f"{player.person_name}'s hand beats the dealer's! {player.person_name} wins!\n")
                            player.chips += int(player.current_bet)
                            if player.chips >= 1000:
                                self.dealer._call_pit_boss()
                                print(f"The pit boss caught {player.person_name} counting cards and removed them from the game!")
                                player.is_still_playing = False
                        elif player_score == dealer_score:
                            player.ties += 1
                            print(f"{player.person_name} ties with the dealer!\n")
                        else:
                            player.losses += 1
                            print(f"The dealer's hand beats {player.person_name}'s. {player.person_name} loses!\n")
                            player.chips -= int(player.current_bet)
                player.hand.discard_hand(self)
        table.dealer.hand.discard_hand(self)
    
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
                table.dealer._deck.deck_of_cards.append(card)
            table.dealer._deck._shuffle()
            table.discard_pile = []
            print(f"There are now {len(table.dealer._deck.deck_of_cards)} cards in the deck.\n")


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
        
        # get post-deal bets
        table.get_player_bets()

        # check for players at the table
        players_playing = table.player_check()

        if players_playing > 0:
            rounds += 1
            print(f"Start of ROUND {rounds}!\n")

            # deal starting hands
            table.dealer.deal_starting_hands(table.player_list)

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
            print(f"{player.person_name} ended the game with {player.chips} chips.  They had {player.wins} wins, {player.ties} ties and {player.losses} losses.")
    else:
        print("Everyone left before the game could even start!")