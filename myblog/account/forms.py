from django import forms


class LoginForm(forms.Form):
    
    '''Форма для в вода пользователя и пароля'''

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)