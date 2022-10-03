from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from Blog.models import BlogContext, Comments, UserProfileInfo
# from django.contrib.auth.models import User


class BlogContextForm(forms.ModelForm):
    class Meta:
        model = BlogContext
        # fields = ('title', 'tag', 'content')
        fields = ('title', 'tag', 'content')
        widgets = {
            # 'publisher': forms.TextInput(attrs={'class': 'textinputclass'}),
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'tag': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }
        error_messages = {
            'title': {'required': "please give the blog a title",},
            'content': {'required': "content cannot be empty",},
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class UserForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # password_confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
        # fields = ('username', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
