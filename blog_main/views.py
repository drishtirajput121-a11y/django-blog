
from django.shortcuts import render
from blogs.models import Category, Blog
from assignments.models import About
def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status="Published")
    post=Blog.objects.filter(is_featured=False, status="Published")

    #Fetch about
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'featured_posts': featured_posts,
        'posts': post,
        'about': about,
    }
    return render(request, 'home.html', context)
