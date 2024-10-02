import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def grab_audio(self) -> sr.AudioData:
        print("何か話してください...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio

    def recognize_audio(self, audio: sr.AudioData) -> str:
        print ("認識中...")
        try:
            speech = self.recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            speech = f"#認識できませんでした"
        except sr.RequestError as e:
            speech = f"#音声認識のリクエストが失敗しました:{e}"
        return speech

    def speech_to_text(self):
        audio = self.grab_audio()
        speech = self.recognize_audio(audio)

        print(speech)

        return speech
