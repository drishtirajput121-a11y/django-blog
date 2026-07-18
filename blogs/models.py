from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class BlogQuerySet(models.QuerySet):
    """Shared query logic — used by template views, the admin dashboard,
    and the DRF API layer, so "what counts as a published/featured post"
    is defined exactly once."""

    def published(self):
        return self.filter(status=Blog.Status.PUBLISHED)

    def featured(self):
        return self.published().filter(is_featured=True)


class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        PUBLISHED = 'Published', 'Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    featured_image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=5000)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogQuerySet.as_manager()

    def __str__(self):
        return self.title

    @classmethod
    def generate_unique_slug(cls, title, exclude_pk=None):
        """One slug algorithm, used by the dashboard views, the API
        ViewSet, and the admin — instead of three copies of the same
        while-loop."""
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        qs = cls.objects.all()
        if exclude_pk:
            qs = qs.exclude(pk=exclude_pk)
        while qs.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
