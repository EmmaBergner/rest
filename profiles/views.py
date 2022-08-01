from django.db.models import Count
from rest_framework import generics, filters
from drf_api.privilege import IsOwerOrReadOnly
from .models import Profile
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProfileSerializers


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializers
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'owner__followed__owner__profile',

    ]

    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',

    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwerOrReadOnly]
    serializer_class = ProfileSerializers
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
