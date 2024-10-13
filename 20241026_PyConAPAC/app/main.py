from datetime import datetime

from genai import GenAI
from schedule import Schedule
from sr import SpeechRecognizer
from tts import TTS

if __name__ == "__main__":
    sr = SpeechRecognizer()
    tts = TTS()
    gen_ai = GenAI()
    while True:
        text = sr.speech_to_text()
        # text = input("Enter text: ")

        if not text:
            continue

        if text == "thank you":
            break
        elif text == "what time is it now":
            response = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        elif "schedule" in text:
            s = Schedule()
            s.auth()
            response = s.execute(text)
            print(response)
            response = gen_ai.generate_content("please answer by natural language" + response)
        else:
            response = gen_ai.generate_content("please answer by natural language" + text)
        print(response)
        tts.say(response)
