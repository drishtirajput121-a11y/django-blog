import django_filters
from blogs.models import Blog


class BlogFilter(django_filters.FilterSet):
    """
    Filter blogs by multiple criteria.
    
    Usage examples:
      ?status=Published
      ?category=3
      ?is_featured=true
      ?created_after=2026-01-01
      ?created_before=2026-12-31
      ?author=1
    """
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Blog
        fields = ['status', 'category', 'is_featured', 'author']
