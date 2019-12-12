import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta

#new

class Category(models.Model):
	name = models.CharField(max_length=30)

class User(models.Model): # seller buyer 구분하지 말고 걍 둘다 가능하게 해
	rating = models.IntegerField(default=0)
	userid = models.CharField(max_length=20, primary_key=True)
	pw = models.CharField(max_length=20) # min length  같은 건 js 단에서 처리하기
	username = models.CharField(max_length=100)
	phone = models.CharField(max_length=30)

class Product(models.Model):
	SELLTYPES = (('F', 'Flea'), ('A', 'Auction'))
	selltype = models.CharField(max_length=1, default='F', choices=SELLTYPES)
	STATUSTYPES = (('S', 'Sold'), ('E', 'Expired'), ('R', 'Running')) # 팔림, 안팔림, 현재진행형
	statustype = models.CharField(max_length=1, default='R', choices=STATUSTYPES)
	EXPIREDATE = (('3', '3 Days'), ('7', '7 days'), ('0', '30 days'))
	expirechoice = models.CharField(max_length=1, default='3', choices=EXPIREDATE)
	expire = models.DateTimeField(default=timezone.now() + timedelta(days=3))
	highest_price = models.IntegerField(default=0) # auction이더라도 천장 가격 내면 바로 살 수 있게 하자
	basic_price =  models.IntegerField(default=0) #옥션이라도 최저가 쓰게 하자
	current_price = models.IntegerField(default=0) # 마지막 가격이기도 하지
	buyer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='buyer', null=True)
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
	pid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=300)
	place = models.CharField(max_length=300)
	photo = models.ImageField(blank=True, null=True) #https://wayhome25.github.io/django/2017/05/10/media-file/
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

	explanation = models.CharField(max_length=1000, null=True) # string field 같은 게 있었나?? 찾아보기

class Wishlist(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	pid = models.ForeignKey(Product, on_delete=models.CASCADE)

class Candidate(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	pid = models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.IntegerField(default=0) # 마지막 가격이기도 하지
	# 플리마켓은 필요없고
	# expire time 끝나는 순간에 보는거야.
	# 야!! 지금 이 expire time인데 wishlist에 이거 넣은놈들 다 나와바
	# 그중에 젤 큰놈? 니가 낙찰이야

# sell history
# 그냥 product에서 userid 같은 거 뽑아내고, 그 pid에서 wishlist 뽑아내면 될것같은데
# buy history는 내가 낙찰된 것만
# 낙찰안된건 알림 오고 치우기

# before


class Customer(models.Model):
	cid = models.CharField(max_length=20, primary_key=True)
	pw = models.CharField(max_length=20)
	birthyear = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(9999)],default=1990)
	GENDERS = (('F', 'Female'), ('M', 'Male'),('U', 'Unknown'))
	gender = models.CharField(max_length=1, default='U', choices=GENDERS)

class History(models.Model):
	pid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateTimeField()

class Book(models.Model):
	isbn = models.CharField(max_length=13, primary_key=True)
	name = models.CharField(max_length=255)
	author = models.CharField(max_length=50)
	price = models.IntegerField(default=0)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Cart(models.Model):
	cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
	isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
	num = models.IntegerField(default=1)

class What(models.Model):
	pid = models.ForeignKey(History, on_delete=models.CASCADE)
	isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
	num = models.IntegerField(default=1)
