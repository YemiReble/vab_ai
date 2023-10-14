from django.conf import settings
from django.http import JsonResponse
from pytube import YouTube
import assmeblyai as asbi
import os


def get_youtube_title(link: str):
    """ The function that handles the youtube title
        operation
    """
    video = YouTube(link)
    title = video.title
    return title
print(get_youtube_title('https://www.youtube.com/watch?v=fxDs4_1Ukg8'))


def get_yt_audio(link: str):
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


def get_yt_transcription(link: str):
    """ The function that gets the transcription of the youtube
        link the user provided
    """
    audio = get_yt_audio(link)
    return audio


def get_something(link: str):
    """ The function that handles the youtube title
        operation
    """
    pass
