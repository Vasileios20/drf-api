from rest_framework import serializers
from .models import Profile, Post


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'content', 'image']
        # fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.ReadOnlyField(source='owner.profile.name')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'content', 'image']
