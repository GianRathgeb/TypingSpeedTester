from modules import time, keyboard


class SpeedTester:
    def __init__(self, text):
        self.text = text
        self.typed_text = ""
        self.stop_waiting = False
        self.mode = "default"
        self.result_time = float

    def start_program(self):
        self.wait("Press the <ENTER> key to start typing: " + str(self.text) + "\n")
        if self.stop_waiting:
            self.start_typing()

    def wait(self, text):
        wait = input(text)
        if wait == "":
            self.stop_waiting = True
        else:
            self.stop_waiting = False

    def start_typing(self):
        starting_time = time.time()
        self.typed_text = input("\n")
        self.result_time = time.time() - starting_time
        print(self.typed_text)
        print(self.result_time)

    def check_text(self):
        pass

    def print_result(self, mode):
        if self.mode == "default":
            print(mode)

