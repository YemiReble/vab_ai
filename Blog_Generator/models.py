from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blog(models.Model):
    """ The User Blog Model
        This is to save the blog post of each user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=400)
    youtube_link = models.URLField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.youtube_title
