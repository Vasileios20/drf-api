from rest_framework import serializers
from .models import Profile, Post


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at', 'updated_at', 'name',
                  'content', 'image', 'is_owner'
                  ]
        # fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.ReadOnlyField(source='owner.profile.name')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'content', 'image']
