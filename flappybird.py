#!/usr/bin/env python

# Flappy Bird Game
# Author: Harmin Patel
# Date Created: 2nd May 2025
# Last Edited: 10th May 2025
# Description: A simple Flappy Bird game using Pygame library

import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/Background.png").convert()
        # Bird images
        self.birdArray = [pygame.image.load("assets/UpsideFlap.png").convert_alpha(),
                            pygame.image.load("assets/DownsideFlap.png").convert_alpha(),
                            pygame.image.load("assets/Dead.png")]
        # Wall images
        self.wallUp = pygame.image.load("assets/Bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/Top.png").convert_alpha()
        self.gap = 160  # Initial gap between the walls
        self.wallx = 400 # Initial position of the wall
        self.birdY = 350 # Initial vertical position of the bird
        self.jump = 0 # Whether the bird is jumping or not
        self.jumpSpeed = 10 # Jump speed
        self.gravity = 5 # Gravity pulling the bird down
        self.dead = False # Flag
        self.array = 0 # Array to pull images depending upon game state
        self.counter = 0 # Score counter
        self.offset = random.randint(-110, 110)

    # Function to update walls when game progresses
    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

            if self.counter % 30 == 0 and self.gap >= 130:  # Minimum gap is 130 to avoid collision
                self.gap -= 3

    # Function to update bird when game progresses
    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY

        # Check for collisions with the walls
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True

        # Check if the bird goes out of bounds
        if not 0 < self.bird[1] < 720:
            self.dead = True
            self.bird[1] = 50
            self.jump = 0
            self.jumpSpeed = 10
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init() # Initialize fonts
        font = pygame.font.SysFont("Arial", 50)
        small_font = pygame.font.SysFont("Arial", 30)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # Close the game if the window is closed

                # Condition to check if the game is over or not 
                if not self.dead:
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.jump = 17
                        self.gravity = 5
                        self.jumpSpeed = 10
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: # Restart the game when 'R' is pressed
                            self.bird = pygame.Rect(65, 50, 50, 50)
                            self.birdY = 350
                            self.jump = 0
                            self.jumpSpeed = 10
                            self.gravity = 5
                            self.dead = False
                            self.array = 0
                            self.counter = 0
                            self.wallx = 400
                            self.offset = random.randint(-110, 110)
                        elif event.key == pygame.K_q: # Quit the game when 'Q' is pressed
                            sys.exit()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), True, (255, 255, 255)), (200, 50))

            if self.dead:
                self.array = 2
            elif self.jump:
                self.array = 1

            self.screen.blit(self.birdArray[self.array], (70, self.birdY))
            if not self.dead:
                self.array = 0
                self.updateWalls()
                self.birdUpdate()

            if self.dead:
                # Game over screen
                # Box dimensions and positions
                box_width, box_height = 350, 225
                box_x = (400 - box_width) // 2
                box_y = (708 - box_height) // 2
                border_radius = 20
                shadow_offset = 5

                # Shadow for message box
                pygame.draw.rect(self.screen, (50, 50, 50), (box_x + shadow_offset, box_y + shadow_offset, box_width, box_height), border_radius=border_radius)
                pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=border_radius)
                pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), width=3, border_radius=border_radius)

                # Game over message and score display
                game_over_text = font.render("Game Over", True, (255, 0, 0))
                score_text = small_font.render(f"Your Score: {self.counter}", True, (0, 0, 0))
                restart_text = small_font.render("Press R to Play Again", True, (0, 0, 0))
                quit_text = small_font.render("Press Q to Quit", True, (0, 0, 0))

                # It display messages in the box
                self.screen.blit(game_over_text, (box_x + (box_width - game_over_text.get_width()) // 2, box_y + 10))
                self.screen.blit(score_text, (box_x + (box_width - score_text.get_width()) // 2, box_y + 80)) 
                self.screen.blit(restart_text, (box_x + (box_width - restart_text.get_width()) // 2, box_y + 130))
                self.screen.blit(quit_text, (box_x + (box_width - quit_text.get_width()) // 2, box_y + 170))
             
            pygame.display.update() # Update the screen display

if __name__ == "__main__":
    FlappyBird().run() 
