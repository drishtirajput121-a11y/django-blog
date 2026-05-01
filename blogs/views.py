from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .models import Blog, Comment
from django.db.models import Q

def category_detail(request, category_id):
    posts = Blog.objects.filter(status='Published', category_id=category_id)
    # try:
    #     category = Category.objects.get(id=category_id)
    # except:
    #     return redirect('home')
    category = get_object_or_404(Category, id=category_id)
    context = {
        'posts': posts,
        'category': category,

    }
    return render(request, 'category_detail.html', context)
def blogs(request, slug):
    single_blog= get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        comment= Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    #comments
    comments = Comment.objects.filter(blog=single_blog)
    comment_count = comments.count()
    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render(request, 'blogs.html',context)

# Create your views here.
def search(request):
    keyword = request.GET.get('keyword')
    blog = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published').distinct()
    context = {
        'blog': blog,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)

def users(request):
    return HttpResponse('Users')