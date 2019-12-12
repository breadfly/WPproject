from django import forms
from .models import Customer
from .models import User
from .models import Product

"""
	SELLTYPES = (('F', 'Flea'), ('A', 'Auction'))
	selltype = models.CharField(max_length=1, default='F', choices=SELLTYPES)
	STATUSTYPES = (('S', 'Sold'), ('E', 'Expired'), ('R', 'Running')) # 팔림, 안팔림, 현재진행형
	statustype = models.CharField(max_length=1, default='E', choices=STATUSTYPES)
	expire = models.DateTimeField(default=0)
	highest_price = models.IntegerField(default=0) # auction이더라도 천장 가격 내면 바로 살 수 있게 하자
	basic_price =  models.IntegerField(default=0) #옥션이라도 최저가 쓰게 하자
	current_price = models.IntegerField(default=0) # 마지막 가격이기도 하지
	buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
	pid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=300)
	place = models.CharField(max_length=300)
	photo = models.ImageField(blank=True) #https://wayhome25.github.io/django/2017/05/10/media-file/
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	explanation = models.CharField(max_length=1000) # string field 같은 게 있었나?? 찾아보기
"""

class SearchForm(forms.Form):
    seller = forms.CharField(required=False,max_length=300, widget=forms.TextInput(attrs={'placeholder':'SELLER'}))
    name = forms.CharField(required=False,max_length=300, widget=forms.TextInput(attrs={'placeholder':'NAME'}))
    lower = forms.IntegerField(required=False,max_length=100, widget=forms.NumberInput(attrs={'placeholder':'LOWER PRICE'}))
    higher = forms.IntegerField(required=False,max_length=100, widget=forms.NumberInput(attrs={'placeholder':'HIGHER PRICE'}))

class MarketPurchaseForm(forms.Form):
    pass

class AuctionPurchaseForm(forms.Form):
    error_css_class = 'error'
    current_price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Price', 'size':'10'}))

class SellForm(forms.ModelForm):
    error_css_class = 'error'

#'selltype', 'expire', 'highest_price', 'basic_price', 'name', 'place', 'photo', 'category', 'explanation'
    class Meta:
        model = Product
        fields = ['selltype', 'expire', 'basic_price', 'name', 'place', 'photo', 'category', 'explanation']

    def __init__(self, *args, **kwargs):
        super(SellForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['explanation'].required = False
        self.fields['photo'].required = False

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
#                self.add_error('userid', "ID already exists")
                return False
            except User.DoesNotExist:
                return valid
                

class LoginForm(forms.ModelForm):
    userid = forms.CharField(required=False,max_length=20, widget=forms.TextInput(attrs={'placeholder':'ID'}))
    pw = forms.CharField(required=False,max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ['userid', 'pw']


class ModifyForm(forms.ModelForm):
    error_css_class = 'error'

    pw = forms.CharField(required=False,max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    username = forms.CharField(required=False,max_length=100, widget=forms.TextInput(attrs={'placeholder':'Name'}))
    phone = forms.CharField(required=False,max_length=30, widget=forms.TextInput(attrs={'placeholder':'Phone Number'}))

    class Meta:
        model = User
        fields = ['pw', 'phone', 'username']
    def is_valid(self):
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
        return valid

 ################

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cid', 'pw', 'birthyear', 'gender']
        widgets = {
            'pw': forms.PasswordInput,
        }


class AddCartForm(forms.Form):
    number = forms.IntegerField(initial=1, min_value=1, max_value=300, required=True)
