from rest_framework import generics, permissions, filters
from drf_api.privilege import IsOwerOrReadOnly
from .models import Comment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CommentSerializers, CommentDetailSerializers


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        ]

    filterset_fields = [
        'post',

    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailSerializers
    permission_classes = [IsOwerOrReadOnly]
    queryset = Comment.objects.all()
