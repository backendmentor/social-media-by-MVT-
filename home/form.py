from django.forms import Form
from django import forms
from .models import POST, Comment

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = POST
        fields = ('content', 'image', 'title',)

class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = POST
        fields = ('content', 'image', 'title',)

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets={
            "content": forms.Textarea(attrs={"class":"form-control"})
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ("content",)



class SearchForm(forms.Form):
    search= forms.CharField()
