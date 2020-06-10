from modules import time, keyboard


class SpeedTester:
    def __init__(self, text):
        self.text = text
        self.input = ""

    def start_program(self):
        if self.wait("Press the <ENTER> key to start typing:\n" + str(self.text)):
            self.start_typing()

    def wait(self, text):
        wait = input(text)
        print(str(wait))
        if wait == "":
            return True

    def start_typing(self):
        self.starting_time = time.time()
        self.input = input("\n")
        self.time = time.time() - self.starting_time
        print(self.input)
        print(self.time)

    def check_text(self):
        pass

    def end_typing(self):
        pass

