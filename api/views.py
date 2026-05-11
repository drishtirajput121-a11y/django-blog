from rest_framework import viewsets, permissions, status, throttling
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from blogs.models import Category, Blog, Comment
from assignments.models import About, SocialLink

from .serializers import (
    CategorySerializer, BlogListSerializer, BlogDetailSerializer,
    CommentSerializer, AboutSerializer, SocialLinkSerializer,
    UserMiniSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardPagination, CommentCursorPagination
from .filters import BlogFilter


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Category ViewSet
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for categories.
    - Anyone can list/retrieve (GET)
    - Only admin can create/update/delete
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['category_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Blog ViewSet — THE MAIN ONE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class BlogViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardPagination
    filterset_class = BlogFilter
    search_fields = ['title', 'short_description', 'blog_body']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        N+1 FIX explained:
        
        WITHOUT this fix, listing 50 blogs would fire:
          1 query for blogs
          + 50 queries for each blog's category
          + 50 queries for each blog's author
          = 101 queries!

        WITH select_related (for ForeignKey):
          Uses SQL JOIN → fetches blog + category + author in 1 query.

        WITH prefetch_related (for reverse ForeignKey):
          Fires 1 extra query to fetch all comments, then caches them.
          Total = 2 queries instead of 101.
        """
        return Blog.objects.select_related(
            'category', 'author'            # FK → uses SQL JOIN (1 query)
        ).prefetch_related(
            'comments', 'comments__user'    # Reverse FK → separate query, cached
        )

    def get_serializer_class(self):
        """Use lightweight serializer for lists, full serializer for detail."""
        if self.action == 'list':
            return BlogListSerializer
        return BlogDetailSerializer

    def perform_create(self, serializer):
        """Auto-set author from JWT token and generate unique slug."""
        title = serializer.validated_data.get('title', '')
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Blog.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        serializer.save(author=self.request.user, slug=slug)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action: GET /api/blogs/{id}/comments/
        Lists all comments for a specific blog with cursor pagination.
        """
        blog = self.get_object()
        comments = Comment.objects.filter(blog=blog).select_related('user')
        paginator = CommentCursorPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Comment ViewSet
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments.
    - Throttled: max 5 comments/minute on create (prevents spam)
    - Only comment owner can edit/delete their comment
    - N+1 fix: select_related for user and blog
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CommentCursorPagination
    throttle_scope = 'comments'

    def get_queryset(self):
        """N+1 fix: always JOIN user and blog data."""
        return Comment.objects.select_related('user', 'blog')

    def get_throttles(self):
        """Apply stricter throttle only when creating comments."""
        if self.action == 'create':
            return [throttling.ScopedRateThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        """Auto-set the comment's user from JWT token."""
        serializer.save(user=self.request.user)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# About & SocialLink ViewSets
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class AboutViewSet(viewsets.ModelViewSet):
    """About section — anyone can read, authenticated can write."""
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SocialLinkViewSet(viewsets.ModelViewSet):
    """Social links — anyone can read, authenticated can write."""
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# User ViewSet (Admin-only, Read-only)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only user list.
    
    Uses IsAdminUser permission — ONLY staff/superusers can access.
    
    IsAuthenticated vs IsAdminUser:
      - IsAuthenticated: any logged-in user (regular + admin)
      - IsAdminUser: only users with is_staff=True
    """
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer
    permission_classes = [permissions.IsAdminUser]
