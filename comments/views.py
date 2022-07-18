from rest_framework import generics, permissions
from drf_api.privilege import IsOwerOrReadOnly
from .models import Comment
from .serializers import CommentSerializers, CommentDetailSerializers


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializers
    permission_classes = [IsOwerOrReadOnly]
    queryset = Comment.objects.all()
