from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    class Meta:
      model = User
      fields = ['username','email', 'password1', 'password2']
      
    # instead of __init__  we use WIDGET_TWEAKS 
    # def __init__(self, *args, **kwargs):
    #   super(UserRegisterForm, self).__init__(*args, **kwargs)
    #   self.fields['username'].widget.attrs.update({'class': 'form-control'})
    #   self.fields['username'].required = True
      
    #   self.fields['email'].widget.attrs.update({'class': 'form-control'})
    #   self.fields['email'].required = True
      
    #   self.fields['password1'].widget.attrs.update({'class': 'form-control'})
    #   self.fields['password1'].required = True
      
    #   self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    #   self.fields['password2'].required = True
         
    