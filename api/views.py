from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.permissions import IsAuthorOrReadOnly
from api.serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from api.models import Post, Follow, Group


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comment_post

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = GroupSerializer


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = FollowSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['=user__username', '=following__username', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
