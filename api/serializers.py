from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Post, Comment, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    text = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', required=False, read_only=True)
    following = serializers.CharField(source='following.username', required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].get('username'))
        follow = Follow.objects.filter(user=self.context['request'].user, following=user).count()
        if user == self.context['request'].user:
            raise serializers.ValidationError("Вы не можете подписаться сам на себя")
        if follow != 0:
            raise serializers.ValidationError("Вы уже подписаны на пользователя")
        return data

    class Meta:
        model = Follow
        fields = ('user', 'following')
