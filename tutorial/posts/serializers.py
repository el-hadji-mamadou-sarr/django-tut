from rest_framework import serializers
from .models import PostModel
from tutorial.users.serializers import UserSerializer

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        author = UserSerializer(read_only=True)
        model = PostModel
        fields = ('title', 'body')    