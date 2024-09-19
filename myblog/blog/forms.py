from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea 
        )

class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment # Получаем форму из модели на прямую
        fields = ['name', 'email', 'body']