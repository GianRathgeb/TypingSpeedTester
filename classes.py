from load_imports import *


class MainWindow:
    def __init__(self):
        # Import settings
        self.settings = ''
        self.get_settings()

        # Settings from file
        self.language = self.settings["LANG"]

        # Get language
        self.languageContent = ''
        self.import_language()

        # Default Settings (Hard coded)
        self.COLOR_HEADER = (255, 213, 102)
        self.COLOR_TEXT = (240, 240, 240)
        self.COLOR_RESULT = (255, 70, 70)
        self.width = 750
        self.height = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.start_time = 0
        self.time_total = 0
        self.accuracy = '0%'
        self.result = self.languageContent["output_results"]

        self.wpm = 0
        self.end = False
        self.background_img_path = './data/img/bg/geometrical.jpg'

        # Init variable used redefined later in the code
        self.time_img = ''
        self.running = False
        self.clock = ''

        # Init pygame
        pygame.init()

        # Loading images

        self.img_open = pygame.image.load('./data/img/loading-screens/loading-gif.gif')
        self.img_open = pygame.transform.scale(self.img_open, (self.width, self.height))

        self.background = pygame.image.load(self.background_img_path)
        # Next line not needed for all images
        # self.background = pygame.transform.scale(self.background, (self.height, self.width))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Typing Speed Tester')

        self.img_settings = pygame.image.load("./data/img/buttons/settings_button.png")
        self.img_settings = pygame.transform.scale(self.img_settings, (50, 50))

        self.img_close = pygame.image.load("./data/img/buttons/close_button.png")
        self.img_close = pygame.transform.scale(self.img_close, (50, 50))

    def get_settings(self):
        # Read settings from file Settings.csv
        with open("./data/settings.csv", "rt") as csvfile:
            file_content = csv.reader(csvfile, delimiter=';')
            # Import Settings
            settings_import = []
            for line in file_content:
                settings_import.append(line)
        self.settings = dict(settings_import)

    # Change settings e.g. Language
    def change_settings(self, option, value):
        with open("./data/settings.csv") as input_file, open("./data/settings_temp.csv", "w", newline='') as output_file:
            settings_content = csv.reader(input_file, delimiter=';')
            writer = csv.writer(output_file)
            for line in settings_content:
                if line[0] == str(option):
                    writer.writerow([str(option) + ';' + str(value)])
                else:
                    writer.writerow([str(line[0]) + ';' + str(line[1])])
        os.remove("./data/settings.csv")
        os.rename("./data/settings_temp.csv", "./data/settings.csv")

    def import_language(self):
        # Loading Language
        path_to_file = "./data/LANG/" + str(self.language) + "/LANG.csv"
        with open(path_to_file, "rt") as langFile:
            lang_file_content = csv.reader(langFile, delimiter=';')
            # Import Settings
            language_import = []
            for line in lang_file_content:
                language_import.append(line)
        self.languageContent = dict(language_import)

    def print_text(self, screen, message, y, font_size, font_color):
        font = pygame.font.Font("./data/fonts/arial.ttf", font_size)
        text = font.render(message, 1, font_color)
        text_rectangle = text.get_rect(center=(self.width/2, y))
        screen.blit(text, text_rectangle)
        pygame.display.update()

    def sentence_get(self):
        f = open('./data/sentences/' + str(self.language) + ".txt").read()
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
            self.result = self.languageContent["output_results"].format(str(round(self.time_total)), str(round(self.accuracy)), str(round(self.wpm)))
            # Draw icon image
            self.time_img = pygame.image.load('./data/img/icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # Screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.width / 2 - 75, self.height - 140))
            self.print_text(screen, self.languageContent["reset"], self.height - 70, 26, (100, 100, 100))
            pygame.display.update()

    def reset_screen(self):
        self.active = False
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
        msg = self.languageContent["title"]
        self.print_text(self.screen, msg, 150, 60, self.COLOR_HEADER)
        # Show image for settings
        self.screen.blit(self.img_settings, (0, 0))
        # Show image for closing
        self.screen.blit(self.img_close, (self.width - 50, 0))
        # Draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        # Draw the sentence string
        self.print_text(self.screen, self.word, 200, 28, self.COLOR_TEXT)
        pygame.display.update()

    def reset_game(self):
        self.screen.blit(self.img_open, (0, 0))
        pygame.display.update()
        time.sleep(0.25)
        self.reset_screen()

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
                    if 0 <= x <= 50 and y <= 50:
                        screen_settings = SettingsWindow(500, 300, self.background_img_path)
                        screen_settings.run_settings()
                        self.language = screen_settings.language
                        self.change_settings("LANG", screen_settings.language)
                        self.import_language()
                        self.width = self.width
                        self.height = self.height
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        pygame.display.set_caption(self.languageContent["title"])
                        self.reset_screen()
                    if self.width - 50 <= x <= self.width and y <= 50:
                        self.running = False
                        sys.exit(0)
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
                    elif not self.active:
                        self.start_time = time.time()
                        self.active = True
                        self.input_text += event.unicode
            pygame.display.update()
        self.clock.tick(60)


class SettingsWindow(MainWindow):
    def __init__(self, width, height, background_img):
        super().__init__()
        self.width = width
        self.height = height
        self.reset = False
        self.end = False

        pygame.display.set_caption(self.languageContent["settings_title"])

        self.img_background = pygame.image.load(background_img)
        self.img_background = pygame.transform.scale(self.img_background, (self.width, self.height))

        self.settings = pygame.display.set_mode((self.width, self.height))

    def load_window(self):
        self.settings.blit(self.img_background, (0, 0))
        # Show image for closing
        self.screen.blit(self.img_close, (self.width - 50, 0))
        self.print_text(self.screen, self.languageContent["settings_title"], 40, 40, self.COLOR_HEADER)
        self.print_text(self.screen, self.languageContent["select_lang"], 80, 20, self.COLOR_TEXT)
        self.screen.fill((0, 0, 0), (100, 100, 350, 50))
        pygame.draw.rect(self.screen, (255, 192, 25), (100, 100, 350, 50), 2)
        pygame.display.update()
        time.sleep(0.25)

    def print_text(self, screen, message, y, font_size, font_color):
        super().print_text(screen, message, y, font_size, font_color)

    def run_settings(self):
        self.load_window()
        self.running = True
        while self.running:
            self.clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (100, 100, 350, 50))
            self.print_text(self.screen, self.input_text.upper(), 124, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    if self.input_text.upper() == "DE":
                        self.language = "LANG_DE"
                    elif self.input_text.upper() == "EN":
                        self.language = "LANG_EN"
                    self.running = False
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if self.width - 50 <= x <= self.width and y <= 50:
                        if self.input_text.upper() == "DE":
                            self.language = "LANG_DE"
                        elif self.input_text.upper() == "EN":
                            self.language = "LANG_EN"
                        self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        try:
                            self.input_text += event.unicode
                        except:
                            pass
                    if len(self.input_text) == 3:
                        self.input_text = self.input_text[:-1]
            pygame.display.update()
        self.clock.tick(60)
