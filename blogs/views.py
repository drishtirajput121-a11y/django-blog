from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .models import Blog

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


# Create your views here.
