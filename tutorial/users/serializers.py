from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tutorial.posts.serializers import PostSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'posts']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

    