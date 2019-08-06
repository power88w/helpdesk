from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def password_match(self,*args,**kwargs):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')
        if password1 is not password2: 
            raise forms.ValidationError("Passwords do not match")
        else:
            return password1