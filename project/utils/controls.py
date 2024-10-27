import pygame


class Controls:
    def __init__(self) -> None:
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.space = pygame.K_SPACE
