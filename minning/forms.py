from django import forms
from django.contrib.auth.models import User


class userForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}),
                               label="", required=True, max_length=50)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email Address'}),
                            label="", required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
                               label="", required=True, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("A user with that Email Address already exists.")
        return data
