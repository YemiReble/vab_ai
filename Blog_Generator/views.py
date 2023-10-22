from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from .models import Blog
import json
from Blog_Generator.functions import (
    get_youtube_audio, 
    get_youtube_title,
    get_youtube_transcription,
    generate_blog_from_openai,
    generate_blog_from_bard,
    generate_blog_from_cohere)


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


def session_logout_user(request):
    """ The function that handles the user logout
        operation
    """
    request.session.flush()
    return redirect('/')


@login_required
def saved_blog(request):
    """ The function that handles the saved blog
        operation
    """
    user_blog = Blog.objects.filter(user=request.user)
    if not user_blog:
        # To be Implimented later in the ftml file
        return render(request, 'saved_blog.html', {'error_message': 'No Blog Found'})

    return render(request, 'saved_blog.html', {'user_blog': user_blog})


def blog_posts(request, pg):
    """ The function that handles the user blog post
    """
    user_blog = Blog.objects.get(id=pg)
    if request.user == user_blog.user:
        return render(request, 'blog_content.html', {'user_blog': user_blog})
    else:
        return redirect('/')


@csrf_exempt
def blog_content(request):
    """ The function that handles the blog content
        operation
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            youtubelink = data['link']
            title = get_youtube_title(youtubelink)

            # Get Transcript
            transcript = get_youtube_transcription(youtubelink)
            if not transcript:
                message = 'Transcription could not be retrieved'
                return JsonResponse({'error': message}, status=400)

            # Get Generated Blog Contents From CohereAI
            gen_content = generate_blog_from_cohere(transcript)
            blog_content = mark_safe(gen_content)
            if not blog_content:
                message = 'Unable to generate blog content'
                return JsonResponse({'error': message}, status=400)

            if len(blog_content) < 40:
                return JsonResponse({'content': blog_content}, status=400)

            else:
                # Save Blog Post
                user_generated_content = Blog(
                        user = request.user,
                        youtube_title = title,
                        youtube_link = youtubelink,
                        content = blog_content
                        )
                user_generated_content.save()

            return JsonResponse({'content': blog_content,
                    'title': title, 'link': youtubelink}, status=200)

        except (json.JSONDecodeError, KeyError):
            message = 'Link not found or data could not be retireved'
            return JsonResponse({'error': message}, status=400)

    else:
        return JsonResponse({'error': 'Invalid Request'}, status=405)
