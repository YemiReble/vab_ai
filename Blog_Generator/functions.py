from django.conf import settings
from django.http import JsonResponse
from pytube import YouTube


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
    try:
        video = YouTube(link)
        audio = video.streams.filter(only_audio=True).first()
        audio_data = audio.download(output_path=settings.MEDIA_ROOT)
        return audio_data
    except Exception:
        return JsonResponse({'error': 'Something went wrong'})


def get_yt_transcription(audio: str):
    """ The function that gets the transcription of the youtube
        link the user provided
    """
    audio = get_yt_audio(audio)
    pass


def get_something(link: str):
    """ The function that handles the youtube title
        operation
    """
    pass
