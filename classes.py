import pygame
from pygame.locals import *
import sys
import time
import random

class SpeedTester:
    def __init__(self):
        self.width = 750
        self.height = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.time_total = 0
        self.accuracy = '0%'
        self.result = 'Time:0 Accuracy:0 % Wpm:0'
        self.wpm = 0
        self.end = False
        self.COLOR_HEADER = (255, 213, 102)
        self.COLOR_TEXT = (240, 240, 240)
        self.COLOR_RESULT = (255, 70, 70)


        pygame.init()
        self.img_open = pygame.image.load('img/type-speed-open.png')
        self.img_open = pygame.transform.scale(self.img_open, (self.width, self.height))


        self.background = pygame.image.load('img/background.jpg')
        self.background = pygame.transform.scale(self.background, (500,750))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Typing Speed Tester')



   