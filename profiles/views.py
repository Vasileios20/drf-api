from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        # data = []
        # for profile in profiles:
        #     data.append(
        #         {
        #             'id': profile.id,
        #             'name': profile.name,
        #             'content': profile.content,
        #             'image': profile.image.url,
        #         }
        #     )
        return Response(serializer.data)
