from rest_framework import serializers
from blogs.models import Category, Blog, Comment
from assignments.models import About, SocialLink
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField(source='blogs.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'blog_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserMiniSerializer(serializers.ModelSerializer):
    """Lightweight user representation for nested use."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class BlogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views (no body, no comments)."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    author = UserMiniSerializer(read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'category', 'category_id',
            'author', 'featured_image', 'short_description',
            'status', 'is_featured', 'comment_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['slug', 'author', 'created_at', 'updated_at']


class BlogDetailSerializer(BlogListSerializer):
    """Full serializer for detail view — includes body + comments."""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(BlogListSerializer.Meta):
        fields = BlogListSerializer.Meta.fields + ['blog_body', 'comments']


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
