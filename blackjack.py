from cards import Deck
from cards import Hand
from players import Person
from players import Player
from players import Dealer
from table import Table
import re

if __name__ == "__main__":

    ## GAME CODE

    # init with player creation
    
    try:
        person = Person('Test')
    except TypeError:
        print("Can't instantiate the abstract Person class!\n")
    
    table = Table()

    #shuffle deck
    table.dealer._deck._shuffle()
    rounds = 0
    # display player info
    print()
    print(f"{'-'*15}INTRODUCTION PHASE{'-'*15}\n")
    print(f"There are {len(table.player_list)} players and a dealer at the table.\n")
    for player in table.player_list:
        player._introduce_self()
    table.dealer._introduce_self()

    # loop while there are still players in the game
    players_playing = 1
    while players_playing > 0:

        # get post-deal bets
        print(f"{'-'*15}BETTING PHASE{'-'*15}\n")
        for player in table.player_list:
            if player.is_still_playing:
                table.get_bet(player)
                print()

        # check for players at the table
        players_playing = 0
        for player in table.player_list:
            if player.is_still_playing:
                players_playing += 1

        if players_playing > 0:
            rounds += 1
            # deal starting hands
            table.dealer.deal_starting_hands(table.player_list)
        
            # show starting hands
            print(f"{'-'*15}STARTING HANDS{'-'*15}\n")
            for person in table.all_people:
                print(f"Cards in {person.person_name}'s hand:")
                person.hand.show_hand()
                print(f"{person.person_name}'s hand is worth {person.hand.calc_score()} points.\n")

            # play each player hand still in game
            print(f"{'-'*15}PLAY PHASE{'-'*15}\n")
            for player in table.player_list:
                if player.is_still_playing:
                    print(f"It's {player.person_name}'s turn to play their hand.")
                    player.hand.show_hand()
                    print(f"{player.person_name}'s hand is worth {player.hand.calc_score()} points.\n")
                    table.play_hand(player)

            all_bust = True
            for player in table.player_list:
                if not player.is_bust:
                    all_bust = False

            if not all_bust:
                # play dealer hand
                table.play_hand(table.dealer)
            
            # compare scores and generate W/T/L against dealer, pay out chips, discard all hands to discard pile
            print(f"{'-'*15}SCORING PHASE{'-'*15}\n")
            if table.dealer.is_bust:
                print("The dealer is bust! All remaining players win!\n")
                for player in table.player_list:
                    if not player.is_bust:
                        player.wins += 1
                        player.chips += int(player.current_bet)
                    player.hand.discard_hand(table)
            else:
                dealer_score = table.dealer.hand.calc_score()
                for player in table.player_list:
                    if player.is_still_playing:
                        if player.is_bust:
                            print(f"{player.person_name} went bust!\n")
                        else:
                            player_score = player.hand.calc_score()
                            if player_score > dealer_score:
                                player.wins += 1
                                print(f"{player.person_name}'s hand beats the dealer's! {player.person_name} wins!\n")
                                player.chips += int(player.current_bet)
                            elif player_score == dealer_score:
                                player.ties += 1
                                print(f"{player.person_name} ties with the dealer!\n")
                            else:
                                player.losses += 1
                                print(f"The dealer's hand beats {player.person_name}'s. {player.person_name} loses!\n")
                                player.chips -= int(player.current_bet)
                    player.hand.discard_hand(table)
            table.dealer.hand.discard_hand(table)

            if len(table.discard_pile) <= 30:
                print(f"There are {len(table.discard_pile)} cards in the discard pile\n")
            else:
                print("Reshuffling the discard pile back in to the deck...\n")
                for card in table.discard_pile:
                    table.dealer._deck.deck_of_cards.append(card)
                table.dealer._deck._shuffle()
                table.discard_pile = []
                print(f"There are now {len(table.dealer._deck.deck_of_cards)} cards in the deck.\n")

        # find players at table, reset variables if they're still playing
        players_playing = 0
        for player in table.player_list:
            if player.is_still_playing:
                player.is_bust = False
                player.current_bet = ''
                players_playing +=1
        table.dealer.is_bust = False

    if rounds > 0 :
        print(f"All players are out of chips or they've left the table. After {rounds} rounds, the game is over!\n")
        print("End of game summary:")
        for player in table.player_list:
            print(f"{player.person_name} ended the game with {player.chips} chips.  They had {player.wins} wins, {player.ties} ties and {player.losses} losses.")
    else:
        print("Everyone left before the game could even start!")

    #TODO: Docstrings and extra stuff?