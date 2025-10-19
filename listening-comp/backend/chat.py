# cohere_chat.py
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from cohere import ClientV2

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("Cohere API key not found in .env")

MODEL_NAME = "command-a-03-2025"  # Latest Cohere chat model

class CohereChat:
    def __init__(self, model_name: str = MODEL_NAME):
        """Initialize Cohere ClientV2 and conversation history"""
        self.client = ClientV2(api_key=COHERE_API_KEY)
        self.model_name = model_name
        self.messages: List[Dict[str, str]] = []

        # Add system message to guide response style
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful assistant. Respond concisely but completely. "
                "Fully answer the user's question in 200-300 tokens. "
                "Don't break abruptly if token limit is reached.finish with the last topic discussed or last sentence reached`.` "
                "Don't overproduce; be relevant and to the point."
            )
        }
        self.messages.append(system_message)

    def generate_response(
        self, message: str, inference_config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """Generate a response using Cohere Chat API v2"""
        if not message.strip():
            return None

        # Default inference config
        temperature = inference_config.get("temperature", 0.7) if inference_config else 0.7
        max_tokens = inference_config.get("max_tokens", 500) if inference_config else 500

        try:
            # Add user message
            self.messages.append({"role": "user", "content": message})

            # Call Cohere Chat API
            response = self.client.chat(
                model=self.model_name,
                messages=self.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Extract assistant reply
            assistant_msg = response.message.content[0].text.strip()

            # Add assistant reply to conversation
            self.messages.append({"role": "assistant", "content": assistant_msg})

            return assistant_msg

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None


if __name__ == "__main__":
    chat = CohereChat()
    print("Chatbot ready! Type '/exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/exit":
            break
        response = chat.generate_response(user_input)
        print("Bot:", response or "(no response)")
