import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[6].id)
        self.engine.setProperty('rate', 150)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
