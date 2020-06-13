from load_imports import *


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
        self.img_open = pygame.image.load('img/loading-screens/loading-gif.gif')
        self.img_open = pygame.transform.scale(self.img_open, (self.width, self.height))

        self.background = pygame.image.load('img/bg/geometrical.jpg')
        # Next line not needed for all images
        # self.background = pygame.transform.scale(self.background, (self.height, self.width))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Typing Speed Tester')

        self.img_settings = pygame.image.load("img/settings_button.png")
        self.img_settings = pygame.transform.scale(self.img_settings, (50, 50))


        # Init variable used redefined later in the code
        self.time_img = ''
        self.running = False
        self.clock = ''

    def print_text(self, screen, message, y, font_size, font_color):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, 1, font_color)
        text_rectangle = text.get_rect(center=(self.width/2, y))
        screen.blit(text, text_rectangle)
        pygame.display.update()

    def sentence_get(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def print_results(self, screen):
        if not self.end:
            # Calculate time
            self.time_total = time.time() - self.start_time
            # Calculate accuracy
            correct_chars = 0
            # Loop through word (counter, letter)
            for counter, value in enumerate(self.word):
                try:
                    if self.input_text[counter] == value:
                        correct_chars += 1
                except:
                    pass
                # Formula for accuracy: (correct characters) / (total characters in sentence) x 100
                # https://www.researchgate.net/post/How_can_I_calculate_the_accuracy
            self.accuracy = correct_chars / len(self.word) * 100
            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.time_total)
            self.end = True
            self.result = "Time: {} secs Accuracy: {}%  Wpm: {}".format(str(round(self.time_total)), str(round(self.accuracy)), str(round(self.wpm)))
            # Draw icon image
            self.time_img = pygame.image.load('img/icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # Screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.width / 2 - 75, self.height - 140))
            self.print_text(screen, "Reset", self.height - 70, 26, (100, 100, 100))
            pygame.display.update()

    def reset_game(self):
        self.screen.blit(self.img_open, (0, 0))
        pygame.display.update()
        time.sleep(0.25)
        # TODO check if code below could replaced by self.__init__()
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.time_total = 0
        self.wpm = 0
        # Get random sentence
        self.word = self.sentence_get()
        if not self.word:
            self.reset_game()
        # Drawing header
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        msg = "Typing Speed Test"
        self.print_text(self.screen, msg, 80, 80, self.COLOR_HEADER)
        # Show image for settings
        self.screen.blit(self.img_settings, (self.width - 50, self.height - 500))
        # Draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        # Draw the sentence string
        self.print_text(self.screen, self.word, 200, 28, self.COLOR_TEXT)
        pygame.display.update()

    def run(self):
        self.reset_game()
        self.running = True
        while self.running:
            self.clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.COLOR_HEADER, (50, 250, 650, 50), 2)
            # Update the text of user input
            self.print_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # Position of input box
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.start_time = time.time()
                    # Position of reset box
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                        sys.exit(0)
                    elif event.key == pygame.K_TAB:
                        self.reset_game()
                    elif self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.print_results(self.screen)
                            self.print_text(self.screen, self.result, 350, 28, self.COLOR_RESULT)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()
        self.clock.tick(60)
