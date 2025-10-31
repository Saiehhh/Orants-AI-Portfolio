# content_extractors.py
import requests
from bs4 import BeautifulSoup
import pdfplumber
import re

def extract_text_from_url(url):
    """
    Extract text content from a web URL.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        if not text:
            raise ValueError("No text content extracted from URL")
        
        print(f"✅ Extracted {len(text)} characters from URL")
        return text
        
    except Exception as e:
        raise Exception(f"Error extracting from URL: {str(e)}")


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise ValueError("No text content extracted from PDF")
        
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error extracting from PDF: {str(e)}")


def extract_from_youtube(url):
    """
    Extract transcript from a YouTube video.
    Accepts both full URLs and video IDs.
    """
    try:
        # Import here to catch any import errors
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Extract video ID from URL
        video_id = url
        if "youtube.com" in url or "youtu.be" in url:
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
                r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    break
        
        print(f"📹 Fetching transcript for video ID: {video_id}")
        
        # Method 1: Try direct retrieval
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get manual transcript first (more accurate)
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
            except:
                # Fallback to generated/auto transcript
                transcript = transcript_list.find_generated_transcript(['en'])
            
            transcript_data = transcript.fetch()
            
        except AttributeError:
            # Method 2: If list_transcripts doesn't exist, try direct method
            print("⚠️ Trying alternative method...")
            import youtube_transcript_api
            transcript_data = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['en', 'en-US', 'en-GB']
            )
        
        # Combine all text
        text = " ".join([entry['text'] for entry in transcript_data])
        
        if not text.strip():
            raise ValueError("No transcript content extracted from YouTube")
        
        print(f"✅ Extracted {len(text)} characters from YouTube video")
        return text.strip()
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ YouTube Error: {error_msg}")
        print("\n💡 Common issues:")
        print("   - Video doesn't have captions/subtitles enabled")
        print("   - Transcripts are disabled by the creator")
        print("   - Video might be age-restricted or private")
        print("\n✅ Try these videos instead:")
        print("   1. https://www.youtube.com/watch?v=JMUxmLyrhSk")
        print("   2. https://www.youtube.com/watch?v=8jPQjjsBbIc")
        print("\n💡 Or use a URL instead:")
        print('   python agent.py --url "https://techcrunch.com/article-url"\n')
        
        raise Exception(f"YouTube extraction failed: {error_msg}")