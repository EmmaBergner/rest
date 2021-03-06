from multiprocessing import context
from django.http import Http404
from requests import delete
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializers
from drf_api.privilege import IsOwerOrReadOnly
from rest_framework import filters

from posts import serializers

class PostList(APIView):
    serializer_clsss = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializers(
            posts, many=True, context={'request' : request}
        )
        return Response(serializer.data)

    
    def post(self, request):
        serializer = PostSerializers(
            data=request.data, context={'request':request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsOwerOrReadOnly]
    serializer_class = PostSerializers

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializers(
            post, context={'request':request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializers(
            post, data = request.data, context={'request':request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

        