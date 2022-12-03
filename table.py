from cards import Deck
from cards import Hand
from players import Player
from players import Dealer
import re

class Table:
    def __init__(self):
        self.player_list = []
        self.dealer = Dealer("Dealy McDealerface")
        self._Table__create_players()
        self.discard_pile = []

    def __create_players(self):
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
        is_valid_bet = False
        player.current_bet = ''
        if player.chips < 10:
            print(f"Looks like you've had a rough night, {player.person_name}! You don't have enough chips to play.")
            player.is_still_playing = False
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
                    table.all_people.remove(player)
                    player.current_bet = 0
                    break
                elif int(player.current_bet) >= 10 and int(player.current_bet) <= player.chips:
                    is_valid_bet = True
                else:
                    print(f"Invalid bet, {player.person_name}!")

    def play_hand(self, player):
        while player.is_still_choosing:
            if player.person_type == 'dealer':
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
        for person in self.all_people:
            print(f"Cards in {person.person_name}'s hand:")
            person.hand.show_hand()

