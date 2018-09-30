import pygame, sys
from Balloon import Balloon
from Button import Button
#from Kitten import Kitten
from random import random

class Engine():

    def __init__(self, screen, settings, scoreboard, balloons, sword):
        self.screen = screen
        self.settings = settings
        self.scoreboard = scoreboard
        self.balloons = balloons
        self.sword = sword

    def release_batch(self):
        for x in range(0, self.settings.batch_size):
            self.spawn_balloon()

    def check_balloons(self, time_passed,x,y):
        # Find any balloons that have been popped,
        #  or have disappeared off the top of the screen
        for balloon in self.balloons:
            balloon.update(time_passed,x,y)

            if balloon.rect.colliderect(self.sword.rect):
                self.pop_balloon(balloon)
                continue

            if balloon.y_position >= 230 + balloon.image_h/2:#+ self.settings.scoreboard_height:
                self.miss_balloon(balloon)
                self.spawn_balloon()
                continue

            balloon.blitme()

        if self.scoreboard.balloons_popped > 0 or self.scoreboard.balloons_missed > 0:
            self.scoreboard.popped_ratio = float(self.scoreboard.balloons_popped)/(self.scoreboard.balloons_popped + self.scoreboard.balloons_missed)
            if self.scoreboard.popped_ratio > self.settings.min_popped_ratio:
                # Set game_active to false, empty the list of balloons, and increment games_played
                #self.settings.game_active = False
                self.settings.games_played += 1

    def update_sword(self, mouse_x, mouse_y):
        # Update the sword's position, and draw the sword on the screen
        self.sword.x_position = mouse_x
        self.sword.y_position = mouse_y
        #else:
           #self.sword.y_position = self.sword.image_h/2 + self.settings.scoreboard_height
        self.sword.update_rect()
        
        self.sword.blitme()

    def pop_balloon(self, balloon):
        self.scoreboard.balloons_missed += 1
        self.balloons.remove(balloon)

    def miss_balloon(self, balloon):
        self.scoreboard.balloons_popped += 1
        self.scoreboard.score += self.settings.points_per_balloon
        self.balloons.remove(balloon)

    def spawn_balloon(self):
        self.balloons.append(Balloon(self.screen, self.settings))
        # Periodically release a kitten:

    def check_events(self, play_button, mouse_x, mouse_y):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sword.rect.collidepoint(mouse_x, mouse_y):
                    self.sword.grabbed = True
                if play_button.rect.collidepoint(mouse_x, mouse_y):
                    # Play button has been pressed.  Empty list of balloons,
                    #  initialize scoreboard and game parameters, and make game active.
                    del self.balloons[:]
                    self.scoreboard.initialize_stats()
                    self.settings.initialize_game_parameters()
                    self.settings.game_active = True
