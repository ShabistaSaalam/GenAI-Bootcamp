# listening_question_generator.py
from typing import Optional
import cohere
import os
from dotenv import load_dotenv
import math

load_dotenv()

class ListeningQuestionGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Cohere client and sets up the base prompt for generating TOPIK-style questions.
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ COHERE_API_KEY not found. Please set it as an environment variable.")

        self.client = cohere.Client(self.api_key)

    def _build_prompt(self, transcript: str, level: int) -> str:
        """
        Build the full prompt text including difficulty instruction
        and generate up to 5 questions based on transcript length.
        """
        sentences = [s for s in transcript.split('.') if s.strip()]
        num_questions = min(10, max(1, math.ceil(len(sentences) / 8)))

        if 1 <= level <= 2:
            difficulty = "Use simple daily-life language for TOPIK I (Level 1–2)."
        elif 3 <= level <= 4:
            difficulty = "Use moderate complexity for TOPIK II (Level 3–4) with natural conversation."
        else:
            difficulty = "Use advanced vocabulary and formal style for TOPIK II (Level 5–6)."

        prompt = f"""
You are a Korean listening comprehension question generator for TOPIK exam preparation.

Given the following Korean listening transcript, generate up to {num_questions} multiple-choice questions.

Requirements:
- Provide the full transcript first (do not split it)
- Questions must be answerable purely from the spoken content
- Write everything in Korean
- Provide 4 answer options per question (1 correct + 3 distractors)
- Mark the correct answer clearly
- Use natural, exam-style phrasing (similar to TOPIK)
- Do NOT translate, explain, or comment
- Follow this format exactly:

<story>
{transcript}
</story>

<question>
Question:
[the question in Korean]

Options:
1. [option 1]
2. [option 2]
3. [option 3]
4. [option 4]

Answer:
[number of the correct option]
</question>
"""
        return prompt

    def generate_question(self, transcript_path: str, output_path: str, level: int = 1) -> None:
        """
        Load transcript → generate questions → save to file.
        """
        transcript = self._load_transcript(transcript_path)
        if not transcript:
            print("❌ Transcript not found or empty.")
            return

        prompt = self._build_prompt(transcript, level)

        try:
            response = self.client.chat(
                model="command-a-03-2025",
                message=prompt,
                temperature=0.6,
                max_tokens=1000  # adjust if needed
            )
            question_text = response.text.strip() if hasattr(response, "text") else None

            if not question_text:
                print("❌ Failed to get a valid response from Cohere.")
                return

            self._save_question(question_text, output_path)
            print(f"✅ Question saved successfully to {output_path}")

        except Exception as e:
            print(f"❌ Error generating question: {e}")

    def _load_transcript(self, path: str) -> Optional[str]:
        """
        Load transcript text from a file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"❌ Error loading transcript: {e}")
            return None

    def _save_question(self, text: str, output_path: str) -> None:
        """
        Save generated questions to a file.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"❌ Error saving question: {e}")


if __name__ == "__main__":
    generator = ListeningQuestionGenerator()

    base_dir = os.path.dirname(__file__)
    transcript_path = os.path.join(base_dir, "transcripts", "6xUxymxl_2k.txt")  # your transcript file
    output_path = os.path.join(base_dir, "questions", "6xUxymxl_2k_questions.txt")  # save file

    generator.generate_question(
        transcript_path=transcript_path,
        output_path=output_path,
        level=2  # choose 1–6 depending on difficulty
    )
