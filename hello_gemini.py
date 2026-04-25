from dotenv import load_dotenv
load_dotenv()

from geminiClient import GeminiClient

client = GeminiClient()
response = client.complete(
    system_prompt="You are a helpful assistant.",
    user_prompt="Say hello in one sentence.",
)

if response:
    print("Gemini integration OK:", response)
else:
    print("ERROR: GeminiClient returned empty string.")
    print("Check that GEMINI_API_KEY in .env is a valid key from https://aistudio.google.com/app/apikey")
