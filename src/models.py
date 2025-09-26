

class Transcript():
    def __init__(self, speaker:str, text:str, start:float, end:float) -> None:
        self.speaker = speaker
        self.text = text
        self.start = start
        self.end = end

    def get_len(self):
        return (self.end-self.start)
