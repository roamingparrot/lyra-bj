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

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit
    if self.rank in ['J', 'Q', 'K']:
            self.rank = 10
    elif self.rank == 'A':
            self.rank = 11

def deck_create():
    deck = [Card(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = sum(card.rank for card in hand)
    number_of_aces = sum(1 for card in hand if card.rank == 11)
    # add ability to adjust the value if there are aces and the total exceeds 21
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

        #not exactly sure why we need event handling but the internet said so :) love you
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
                elif event.key == pygame.K_s:  # Player stands
                    player_turn = False

        
        if not player_turn and not game_over:
            while calculate_hand_value(dealer_hand) <= 17:
                dealer_hand.append(deck.pop())
            if calculate_hand_value(dealer_hand) > 21:
                dealer_busted = True
                game_over = True
            else:
                game_over = True
                
            