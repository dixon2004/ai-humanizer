from utils.logger import SyncLogger
from google.genai import types
from google import genai


class GoogleGemini:

    def __init__(self, api_key: str) -> None:
        """
        Initialize the Google Gemini API client.

        Args:
            api_key (str): The API key for Google Gemini.
        """
        self.client = genai.Client(api_key=api_key)
        self.logger = SyncLogger(class_name="GoogleGemini")
        self.prompt = self._load_prompt()


    def _load_prompt(self) -> str:
        """
        Load the prompt from a file.
        
        Returns:
            str: The loaded prompt.
        """
        try:
            with open("prompts/humanizer.txt", "r") as file:
                return file.read()
        except Exception as e:
            self.logger.write_log("error", f"Failed to load prompt file: {e}")
            raise e


    def generate_content(self, model: str = "gemini-2.5-flash-preview-04-17", content: str = "", temperature: float = 0.7) -> str:
        """
        Generate content using the Google Gemini API.

        Args:
            model (str): The model to use for content generation.
            content (str): The content to generate.
            temperature (float): The temperature for content generation.

        Returns:
            str: The generated content.
        """
        try:
            full_prompt = f"{self.prompt}\n\nText:\n{content}"

            system_instruction = "You rewrite content to sound more human and natural."

            response = self.client.models.generate_content(
                model=model, contents=[full_prompt],
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system_instruction
                )
            )
            return response.text
        except Exception as e:
            self.logger.write_log("error", f"Failed to generate content: {e}")
            raise e
