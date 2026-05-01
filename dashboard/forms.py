from django import forms
from blogs.models import Blog, Category, User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = {'title', 'category', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured'}

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups','user_permissions')
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups','user_permissions')