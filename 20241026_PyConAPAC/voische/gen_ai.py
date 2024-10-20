import google.generativeai as genai

GOOGLE_API_KEY=""


class GenAI:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.genai = genai.GenerativeModel("gemini-pro")

    def generate_content(self, prompt: str) -> str:
        try:
            response = self.genai.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred"

if __name__ == "__main__":
    gen_ai = GenAI()
    prompt = input("Prompt: ")
    print(gen_ai.generate_content(prompt))
