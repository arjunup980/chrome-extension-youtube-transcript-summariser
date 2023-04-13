import logging
import subprocess
import re
from django.conf import settings
import openai
import pytube
import youtube_transcript_api
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import ssl
from django.core.cache import cache

from transcript.decorators import log_time

ssl._create_default_https_context = ssl._create_stdlib_context


logger = logging.getLogger(__name__)

class TranscriptService:

    @staticmethod
    @log_time
    def get_transcript(video_id: str) -> str:

        # Fetch the transcript for the video
        try:
            logger.info(f"Fetching transcript for video ID: {video_id}")
            transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
            transcript = '\n'.join([t['text'] for t in transcript_list])
        except Exception as exc:
            logger.error(f"Error fetching transcript for video ID: {video_id}")
            transcript = ""

        return transcript

    @staticmethod
    @log_time
    def get_openai_summary(text: str, title) -> str:

        title_prompt = f"Generate the summary that answers the tite: {title}"

        # Authenticate with OpenAI API
        openai.api_key = settings.OPENAI_KEY

        # Send the transcript to OpenAI
        logger.info(f"Sending transcript to OpenAI for summarization")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": f"below is my youtube transcript summary with tile. Assume you are a excellent english professor. rewrite the summary provided in a consicise way \
                        and in 2-3 para. {title_prompt}"},
                        {"role": "user", "content": text},
                    ]
            )
            summary = ''
            for choice in response.choices:
                summary += choice.message.content
        except Exception as exc:
            logger.warning("Error from openai: {exc}")
            summary = "Loaded with requests. Kindly try later!"

        return summary

    @staticmethod
    @log_time
    def get_nlp_model(model="en_core_web_sm"):
        try:
            logger.info(f"Loading spacy model: {model}")
            nlp = spacy.load(model)
            logger.info(f"Loaded spacy model: {model}")
        except Exception as exc:
            logger.error(f"Error loading spacy model: {model}")
            logger.error(f"Downloading spacy model: {model}")
            subprocess.run(['python', '-m', 'spacy', 'download', model])
            logger.info(f"Downloaded spacy model: {model}")
            nlp = spacy.load(model)
            logger.info(f"Loaded spacy model: {model}")
        
        return nlp

    @log_time
    def get_nlp_summary(self, text, per):
        nlp = self.get_nlp_model()
        doc= nlp(text)

        logger.info(f"Generating summary using spacy")
        word_frequencies={}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS):
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        max_frequency=max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word]=word_frequencies[word]/max_frequency
        sentence_tokens= [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():                            
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]
        select_length=int(len(sentence_tokens)*per)
        summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)
        return summary

    @log_time
    def get_summary(self, youtube_url, refresh=False):

        # Extract the video ID from the URL using regex
        match = re.search(r'(?<=v=)[^&]+', youtube_url)
        video_id = match.group(0) if match else None
        
        # return response from cache if available
        summary=cache.get(video_id)
        if summary and not refresh:
            return {"summary": summary}


        if not video_id:
            logger.error(f"Invalid YouTube URL: {youtube_url}")
            return {'error': 'Invalid YouTube URL'}

        transcript = self.get_transcript(video_id=video_id)

        if not transcript:
            return "Unable to fetch video transcript. Subtitles are required! Check for the subtitle in the video!"
        
        nlp_summary = self.get_nlp_summary(transcript, per=0.45)

        try:
            title = pytube.YouTube(f'https://www.youtube.com/watch?v={video_id}').title
        except Exception as exc:
            logger.warning(f"Unable to get video title: {exc}")
            title = ""
            
        summary = self.get_openai_summary(text=nlp_summary[:3000], title=title)

        # set the cache if summary is not null
        if len(summary) > 0:
            cache.set(video_id, summary, timeout=86400)
            
        # Return the OpenAI response
        return {"summary": summary}
