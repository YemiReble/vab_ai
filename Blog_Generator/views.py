from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from Blog_Generator.functions import (
    get_youtube_audio, 
    get_youtube_title,
    get_youtube_transcription,
    generate_blog_from_openai)


# Create your views here.
@login_required
def index(request):
    """ This function returns or render the index
        page of this Application
    """
    return render(request, 'index.html')

def user_login(request):
    """ The function that handles all users login
        operation
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html',
                          {'error_message': 'Invalid cridentials'})
        
    return render(request, 'login.html')

def user_signup(request):
    """ The function that handles the user signup
        operation
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeatpassword']

        # Check if password is and repeated password are alike
        if password != repeat_password:
             return render(request, 'signup.html',
                        {'error_message': 'Please check your password',})
        else:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                return render(request, 'signup.html',
                        {'error_message': 'Error creating your account',})

    return render(request, 'signup.html')

def user_logout(request):
    """ The function that handles the user logout
        operation
    """
    logout(request)
    return redirect('/')

def saved_blog(request):
    """ The function that handles the saved blog
        operation
    """
    return render(request, 'saved_blog.html')

@csrf_exempt
def blog_content(request):
    """ The function that handles the blog content
        operation
    """
    if request.method == 'POST':
        try:
            data = json.load(request.body)
            youtubelink = data['link']
            title = get_youtube_title(youtubelink)
            
            # Get Transcript
            transcript = get_youtube_transcription(youtubelink)
            if not transcript:
                message = 'Transcription could not be retrieved'
                return JsonResponse({'error': message}, status=400)
            
            # Get Generated Blog Contents From Bard
            blog_content = generate_blog_from_bard(transcript)
            if not blog_content:
                message = 'Unable to generate blog content'
                return JsonResponse({'error': message}, status=400)
                

            return JsonResponse({'content': youtubelink}, status=200)

        except (json.JSONDecodeError, KeyError):
            message = 'Link not found or data could not be retireved'
            return JsonResponse({'error': message}, status=400)

    else:
        return JsonResponse({'error': 'Invalid Request'}, status=405)
