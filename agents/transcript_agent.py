from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from .base_agent import BaseAgent

class TranscriptAgent(BaseAgent):
    def __init__(self):
        super().__init__("transcript_agent")

    def get_video_id(self, url):
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
        return None

    def fetch_from_url(self, url):
        """Fetch transcript from YouTube URL"""
        video_id = self.get_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])
            
            # Save the transcript for debugging
            self.save_output(transcript_text, 'transcript.txt')
            
            return transcript_text
        except Exception as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")

    def process(self, input_data):
        """Process either URL or direct transcript input"""
        if input_data.startswith('http'):
            return self.fetch_from_url(input_data)
        return input_data
