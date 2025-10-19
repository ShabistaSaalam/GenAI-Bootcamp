from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict
import os


class YouTubeTranscriptDownloader:
    def __init__(self, languages: List[str] = ["ko", "en"]):
        self.languages = languages
        self.api = YouTubeTranscriptApi()  # new instance-based API

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.
        """
        if "v=" in url:
            return url.split("v=")[1][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        return None

    def get_transcript(self, video_id: str) -> Optional[List[Dict]]:
        """
        Download YouTube transcript using the new API.
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)

        if not video_id:
            print("❌ Invalid video ID or URL")
            return None

        print(f"📥 Downloading transcript for video ID: {video_id}")

        try:
            # Fetch transcript (returns FetchedTranscript)
            fetched_transcript = self.api.fetch(video_id, languages=self.languages)
            # Convert to list of dicts
            return fetched_transcript.to_raw_data()
        except Exception as e:
            print(f"❌ Error fetching transcript: {str(e)}")
            return None

    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file.
        """
        try:
            # Absolute path inside project folder
            base_dir = os.path.join(os.getcwd(), "backend","transcripts")
            os.makedirs(base_dir, exist_ok=True)

            filepath = os.path.join(base_dir, f"{filename}.txt")

            with open(filepath, "w", encoding="utf-8") as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")

            print(f"✅ Transcript saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error saving transcript: {str(e)}")
            return False


def main(video_url: str, print_transcript: bool = False):
    downloader = YouTubeTranscriptDownloader()

    transcript = downloader.get_transcript(video_url)
    if transcript:
        video_id = downloader.extract_video_id(video_url)
        if downloader.save_transcript(transcript, video_id):
            print(f"✅ Transcript saved successfully to ./transcripts/{video_id}.txt")

            if print_transcript:
                print("\n📝 Transcript Preview:\n")
                for entry in transcript:
                    print(entry["text"])
        else:
            print("❌ Failed to save transcript")
    else:
        print("❌ Failed to get transcript")


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=73LaRgBlvJg&list=PLJ8SeVAoE0L4cGkmhuRHIpWGOgY3SCwYL&index=3"
    main(video_url, print_transcript=True)
