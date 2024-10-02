from datetime import datetime

from sr import SpeechRecognizer
from tts import TTS

if __name__ == "__main__":
    sr = SpeechRecognizer()
    tts = TTS()
    while True:
        text = sr.speech_to_text()
        if text == "thank you":
            break
        elif text == "what time is it now":
            text = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        tts.say(text)
