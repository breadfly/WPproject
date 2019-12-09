from django import forms
from .models import Customer
from .models import User

class RegisterForm(forms.ModelForm):
    error_css_class = 'error'

    userid = forms.CharField(required=False,max_length=20, widget=forms.TextInput(attrs={'placeholder':'ID'}))
    pw = forms.CharField(required=False,max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    username = forms.CharField(required=False,max_length=100, widget=forms.TextInput(attrs={'placeholder':'Name'}))
    phone = forms.CharField(required=False,max_length=30, widget=forms.TextInput(attrs={'placeholder':'Phone Number'}))
    class Meta:
        model = User
        fields = ['userid', 'pw', 'username', 'phone']

    def is_valid(self):
        userid=str(self.data['userid'])
        pw=str(self.data['pw'])
        username=str(self.data['username'])
        phone=str(self.data['phone'])

        valid = True

        if len(pw) > 20 :
            self.add_error('pw', "Password length should be 20 or less")
            valid= False
        elif len(pw) < 4 :
            self.add_error('pw', "Password length should be 4 or more")
            valid= False
        elif pw.isalnum() == False :
            self.add_error('pw', "Password should include only letters and numbers")
            valid= False
        elif pw.isdigit() == True or pw.isalpha() == True:
            self.add_error('pw', "Password must contain at least one number and one letter.")
            valid =False

        if len(username) > 100 :
            self.add_error('username', "Name length should be 100 or less")
            valid= False
        elif len(username) < 1 :
            self.add_error('username', "Name length should be 1 or more")
            valid= False
        elif username.isalnum() == False :
            self.add_error('username', "Name should include only letters and numbers")
            valid= False

        if phone.isdigit() == False:
            self.add_error('phone', "Phone number should include only numbers")
            valid= False

        if len(userid) > 20 :
            self.add_error('userid', "ID length should be 20 or less")
            valid = False
        elif len(userid) < 4 :
            self.add_error('userid', "ID length should be 4 or more")
            valid= False
        elif userid.isalnum() == False :
            self.add_error('userid', "ID should include only letters and numbers")
            valid = False
        else:
            try:
                user = User.objects.get(userid=userid)
                self.add_error('id', "ID already exists")
                return False
            except User.DoesNotExist:
                return valid
                

class LoginForm(forms.ModelForm):
    userid = forms.CharField(required=False,max_length=20, widget=forms.TextInput(attrs={'placeholder':'ID'}))
    pw = forms.CharField(required=False,max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ['userid', 'pw']

 ################

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


class AddCartForm(forms.Form):
    number = forms.IntegerField(initial=1, min_value=1, max_value=300, required=True)
