from .models import Category
from assignments.models import SocialLink

def get_categories(request):
    return dict(categories=Category.objects.all())

def get_social_links(request):
    return dict(social_links=SocialLink.objects.all())