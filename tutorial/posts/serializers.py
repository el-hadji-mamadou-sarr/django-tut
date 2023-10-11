from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostModel
        fields = ('title', 'body')    