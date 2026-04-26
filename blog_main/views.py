
from django.shortcuts import render
from blogs.models import Category, Blog
def home(request):
    catogories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status="Published")
    post=Blog.objects.filter(is_featured=False, status="Published")
    context = {
        'categories': catogories,
        'featured_posts': featured_posts,
        'posts': post,
    }
    return render(request, 'home.html', context)
