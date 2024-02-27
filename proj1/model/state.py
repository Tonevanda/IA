import pygame

class State:
    def __init__(self, size):
        player1 = 'Orange'
        player2 = 'Blue'
        current_player = player1
    
    def make_move(self, pos, board):
        