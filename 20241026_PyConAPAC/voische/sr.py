import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def grab_audio(self) -> sr.AudioData:
        print("Listening...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio

    def recognize_audio(self, audio: sr.AudioData) -> str | None:
        print ("Recognizing...")
        try:
            return self.recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"An error occurred: {e}")

    def speech_to_text(self):
        audio = self.grab_audio()
        speech = self.recognize_audio(audio)

        print(speech)

        return speech

if __name__ == "__main__":
    sr = SpeechRecognizer()
    while True:
        sr.speech_to_text()
