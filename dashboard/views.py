from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, PostForm, UserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})


@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {'form': form, 'category': category})


@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':           # ✅ only delete on POST
        category.delete()
        return redirect('categories')
    return redirect('categories')          # GET just redirects safely


@login_required(login_url='login')
def posts(request):
    posts = Blog.objects.all()
    return render(request, 'dashboard/posts.html', {'posts': posts})


@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            post.slug = slug
            post.save()
            return redirect('posts')
    form = PostForm()
    return render(request, 'dashboard/add_post.html', {'form': form})


@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if post.author != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)       # ✅ get updated object first

            base_slug = slugify(post.title)      # ✅ now uses NEW title
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=post.pk).exists():  # ✅ exclude self
                slug = f"{base_slug}-{counter}"
                counter += 1

            post.slug = slug
            post.save()                          # ✅ saves form data + slug
            return redirect('posts')
    form = PostForm(instance=post)
    return render(request, 'dashboard/edit_post.html', {'form': form, 'post': post})


@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if post.author != request.user:
        return redirect('home')
    if request.method == 'POST':               # ✅ POST only
        post.delete()
        return redirect('posts')
    return redirect('posts')


@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})


@login_required(login_url='login')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = UserForm()
    return render(request, 'dashboard/add_user.html', {'form': form})


@login_required(login_url='login')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    return render(request, 'dashboard/edit_user.html', {'form': form, 'user': user})


@login_required(login_url='login')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':               # ✅ POST only
        user.delete()
        return redirect('users')
    return redirect('users')
