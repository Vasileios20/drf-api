from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset(comments) or creating a model instance.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]
