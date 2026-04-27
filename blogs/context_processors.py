from .models import Category

def get_categories(request):
    return dict(categories=Category.objects.all())