from modules import time, keyboard


class SpeedTester:
    def __init__(self, text):
        self.text = text
        self.input = ""
        self.fails = 0

    def start_program(self):
        if self.wait("Press the <ENTER> key to start typing:\n" + str(self.text)):
            self.start_typing()
            self.end_typing()
            self.check_text()

    def wait(self, text):
        wait = input(text)
        print(str(wait))
        if wait == "":
            return True

    def start_typing(self):
        self.starting_time = time.time()
        self.input = input("\n")


    def check_text(self):
        for i in range (0, len(self.input)):
            if self.text[i] != self.input[i]:
                self.fails += 1
                # TODO Write function to check if text is correct and how many fails
            else:
                pass # Do nothing
        print(self.fails)
                

    def end_typing(self):
        self.time = time.time() - self.starting_time
        print(self.input)
        print(self.time)

