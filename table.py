from cards import Deck
from cards import Hand
from players import Player
from players import Dealer

class Table:
    def __init__(self):
        self.player_list = []
        self.dealer = Dealer("Dealy McDealerface")
        self._Table__create_players()
        self.discard_pile = []

    def __create_players(self):
        self.all_people = []
        print("This game will allow for a maximum of 3 players.")
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
        self.all_people.append(self.dealer)
        for player in self.player_list:
            self.all_people.append(player)

    def get_bet(self, player):
        player.current_bet = 0
        if player.chips < 10:
            print("Looks like you've had a rough night. You don't have enough chips to play!")
            player.still_playing = False
        else:
            print(f"How much would you like to bet, {player.person_name}?")   
            player.current_bet = input(f"Minimum bet is 10, maximum bet is {player.chips}, or enter 'x' to leave the table > ")
            while player.current_bet.strip().lower() not in ['x']:
                while(player.current_bet < 10 or player.current_bet > player.chips):
                    player.current_bet = input(f"Invalid bet, {player.person_name}! Minimum bet is 10, maximum bet is {player.chips} > ")
            if player.current_bet == 'x':
                player.is_still_playing = False
                print(f"Thanks for playing, {player.person_name}!")
                #### Do more stuff to dump the player and their cards from the game here
                table.all_people.remove(player)
            else: player.current_bet = int(player.current_bet)

    def play_hand(self, player):
        while player.is_still_choosing:
            player._hit_or_stand(player)
            if player.is_still_choosing:
                player.hand.add_card(table.dealer._deck.deal())
                player.hand.show_hand()
            else:
                player.is_still_choosing = True # resetting for next round
                break
            if player.hand.calc_score() > 21:
                print(player.hand.calc_score())
                print(f"{player.person_name} has more than 21 and they've busted!")
                player.is_bust = True
                break

    def show_all_hands(self):
        for person in self.all_people:
            print(f"Cards in {person.person_name}'s hand:")
            person.hand.show_hand()


table = Table()
print(f"There are {len(table.player_list)} players at the table.")
for player in table.player_list:
    player._introduce_self()
    print()
table.dealer._introduce_self()
table.dealer.deal_starting_hands(table.player_list)

print(f"Table all people length {len(table.all_people)}")
for person in table.all_people:
    print(f"Cards in {person.person_name}'s hand:")
    person.hand.show_hand()

print(f"There are {len(table.player_list)} players")
for player in table.player_list:
    if player.is_still_playing:
        table.get_bet(player)

for player in table.player_list:
    table.play_hand(player)

#TODO: finish out the section for allowing individual player to quit, finish out game sequence and then incorporate it into a loop that can run until all players are broke or have left
