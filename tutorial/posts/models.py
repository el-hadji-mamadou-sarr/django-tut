from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def get_default_author():
    user = User.objects.get_or_create(username='admin')[0]
    return user.id

class PostModel (models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=get_default_author())

    def __str__(self) :
        return self.title
