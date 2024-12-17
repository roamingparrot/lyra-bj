import pygame
pygame.init()
import random
import sys

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont("Arial", 28)
WHITE = (255, 255, 255)
GREEN = (78, 106, 84)

def display_text(text, x, y, color=WHITE):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

def display_hand(hand, x, y):
    for i, card in zip(range(len(hand)), hand):
        display_text(f'{card.rank} of {card.suit}', x, y + i * 30)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if self.rank in ['J', 'Q', 'K']:
            self.value = 10
        elif self.rank == 'A':
            self.value = 11
        else:
            self.value = int(self.rank)


def deck_create():
    deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = sum(card.value for card in hand)
    number_of_aces = sum(1 for card in hand if card.rank == 'A')
    if value > 21 & number_of_aces > 0:
        value = value - 10
        number_of_aces = number_of_aces - 1
    return value

def main():
    running = True
    clock = pygame.time.Clock()

    deck = deck_create()
    player_hand = []
    dealer_hand = []

    player_turn = True
    game_over = False
    player_busted = False
    dealer_busted = False

    player_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    while running:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if player_turn and not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h: 
                        player_hand.append(deck.pop())
                        if calculate_hand_value(player_hand) > 21:
                            player_busted = True
                            game_over = True
                    elif event.key == pygame.K_s:
                        player_turn = False

      
        if not player_turn and not game_over:
            while calculate_hand_value(dealer_hand) <= 17:
                dealer_hand.append(deck.pop())
            if calculate_hand_value(dealer_hand) > 21:
                dealer_busted = True
            game_over = True

      
        display_hand(player_hand, 50, 100)
        display_hand(dealer_hand, 500, 100)

        if game_over:
            if player_busted:
                display_text("Player Busted! Dealer Wins!", 50, 400)
            elif dealer_busted:
                display_text("Dealer Busted! Player Wins!", 50, 400)
            else:
                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)
                if player_value > dealer_value:
                    display_text("Player Wins!", 50, 400)
                elif player_value < dealer_value:
                    display_text("Dealer Wins!", 50, 400)
                else:
                    display_text("It's a Tie!", 50, 400)
            display_text("Press ESC to exit.", 50, 450)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.flip() 
        clock.tick(60) 

    pygame.quit()
    sys.exit()

main()
