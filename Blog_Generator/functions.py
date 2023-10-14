from django.conf import settings
from django.http import JsonResponse
from pytube import YouTube
import assemblyai as aai
from secret import assemblyal_key, openai_key
import openai
import os


def get_youtube_title(link: str):
    """ The function that handles the youtube title
        operation
    """
    video = YouTube(link)
    title = video.title
    return title


def get_youtube_audio(link: str):
    """ The function that gets and downloads the audio of the youtube
        link the user provided
    """
    video = YouTube(link)
    audio = video.streams.filter(only_audio=True).first()
    audio_data = audio.download(output_path=settings.MEDIA_ROOT)
    base, extention = os.path.splitext(audio_data)
    downl_file = base + '.mp3'
    os.rename(audio_data, downl_file)
    return downl_file


def get_youtube_transcription(audio_path: str):
    """ The function that gets the transcription of the youtube
        link the user provided
    """
    aai.settings.api_key = assemblyal_key
    audio = get_youtube_audio(audio_path)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio)
    return transcript.text


def generate_blog_from_openai(transcript: str):
    """ The function that handles the youtube title
        operation
    """
    openai.api_key = openai_key
    
    prompt = f'Base on the following transcript from a YouTube video, generate a\
        comprehensive blog article using the transcript and do not make it look like it is\
            from a YouTube video:\n\n{transcript}\n\nArticle:'
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
    )

    blog_content = response.choices[0].text.strip()
    return blog_content