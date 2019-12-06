from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cid', 'pw', 'birthyear', 'gender']
        widgets = {
            'pw': forms.PasswordInput,
        }

class ModifyForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['pw', 'birthyear', 'gender']
        widgets = {
            'pw': forms.PasswordInput,
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cid', 'pw']
        widgets = {
            'pw': forms.PasswordInput,
        }

class AddCartForm(forms.Form):
    number = forms.IntegerField(initial=1, min_value=1, max_value=300, required=True)
