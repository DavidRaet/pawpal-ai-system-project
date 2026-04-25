import os 


class GeminiClient:
    """
    Minimal Gemini API wrapper with added error resilience.

    Requirements:
    - google-genai installed
    - GEMINI_API_KEY set in environment (or loaded via python-dotenv)
    """

    def __init__(self, model_name: str = "gemma-3-27b-it", temperature: float = 0.2):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY. Create a .env file and set GEMINI_API_KEY=..."
            )

        # Import here so heuristic mode doesn't require the dependency at import time.
        from google import genai

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = float(temperature)

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a single request to Gemini.

        If an error occurs, it returns an empty string, triggering the agent's
        heuristic fallback logic.
        """
        try:
            merged_prompt = f"{system_prompt}\n\n{user_prompt}".strip()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=merged_prompt,
            )

            # Defensive: response.text can be None or raise an error if blocked by filters.
            return response.text or ""

        except Exception:
            # Returning empty string allows the agent to detect the failure
            # and switch to offline rules.
            return ""
