from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('savedblog/', views.saved_blog, name='saved_blog'),
    path('blogcontent/', views.blog_content, name='blog_content'),
    path('blogposts/<int:pg>', views.blog_posts, name='blog_posts'),
]
