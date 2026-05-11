from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination, CursorPagination
)


class StandardPagination(PageNumberPagination):
    """
    Default pagination style: ?page=2
    Client can override page size: ?page_size=25
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardLimitOffsetPagination(LimitOffsetPagination):
    """
    Alternative pagination: ?limit=10&offset=20
    Good for mobile apps that need flexible jumping.
    """
    default_limit = 10
    max_limit = 100


class CommentCursorPagination(CursorPagination):
    """
    Cursor-based pagination for comments.
    Best for infinite scroll / real-time feeds.
    Uses opaque cursor — no page jumping possible.
    """
    page_size = 20
    ordering = '-created_at'
