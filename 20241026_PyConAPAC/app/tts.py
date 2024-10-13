import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', "english-us")
        self.engine.setProperty('rate', 180)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    # tts = TTS()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        print(v)
    engine.setProperty('voice', "english-us")
    engine.setProperty('rate', 150)
    engine.say("this is a pen")
    engine.runAndWait()