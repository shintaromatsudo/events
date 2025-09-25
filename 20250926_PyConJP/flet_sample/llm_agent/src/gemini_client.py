from google import genai


class GeminiClient:
    """Gemini API とのやりとりを管理するクラス"""

    def __init__(self):
        self.client = genai.Client()

    def generate_content_stream(self, message: str):
        response = self.client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=[message],
        )

        return response
