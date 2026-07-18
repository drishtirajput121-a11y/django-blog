from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Blog, Comment
from django.db.models import Q


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Blog.objects.published().filter(category_id=category_id)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'category_detail.html', context)


def blogs(request, slug):
    """Renders a single published post. Comments are no longer handled
    here — the page loads/creates them via the DRF API
    (see templates/blogs.html), so there's one place that owns
    comment-creation logic instead of two."""
    single_blog = get_object_or_404(Blog, slug=slug, status=Blog.Status.PUBLISHED)
    comment_count = Comment.objects.filter(blog=single_blog).count()
    context = {
        'single_blog': single_blog,
        'comment_count': comment_count,
    }
    return render(request, 'blogs.html', context)


def search(request):
    keyword = request.GET.get('keyword', '').strip()
    if keyword:
        blog = Blog.objects.published().filter(
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword)
        ).distinct()
    else:
        blog = Blog.objects.none()
    context = {
        'blog': blog,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)


def users(request):
    return HttpResponse('Users')
