from django.db.models import Count
from .models import Post
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializers
from drf_api.privilege import IsOwerOrReadOnly
from rest_framework import generics, filters, permissions


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializers
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    #Search for country
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
        ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
        ]

    search_fields = [
        'owner__username',
        'title',
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwerOrReadOnly]
    serializer_class = PostSerializers
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    

        