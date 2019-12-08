import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator z

#new

"""
추가하면 좋을 기능 정리
1. auction이더라도 바로 낙찰할 수 있는 가격 / highest
구매자가 너무 맘에 들어서 이 가격 써내면 바로 낙찰됨
2. 최저가 설정도 하게 하기
3. 언제까지 팔 건지 시간 선택 가능.
4. 카테고리
5. 다양한 정렬 기능 (방금 입찰된 것, 가장 많이 입찰된 것 등등)
6. 판매자 평가 기능(낙찰자만 가능)
7. 입찰한 사람이 아무도 없을 경우에만 expire 늘릴 수 있음
8. 낙찰 알림페이지
"""

class Product(models.Model):
	SELLTYPES = (('F', 'Flea'), ('A', 'Auction'))
	selltype = models.CharField(max_length=1, default='F', choices=SELLTYPES)
	STATUSTYPES = (('S', 'Sold'), ('E', 'Expired'), ('R', 'Running')) # 팔림, 안팔림, 현재진행형
	statustype = models.CharField(max_length=1, default='E', choices=STATUSTYPES)
	expire = models.DateTimeField(default=0)
	highest_price = models.IntegerField(default=0) # auction이더라도 천장 가격 내면 바로 살 수 있게 하자
	basic_price =  models.IntegerField(default=0) #옥션이라도 최저가 쓰게 하자
	current_price = models.IntegerField(default=0) # 마지막 가격이기도 하지
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	pid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=300)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	place = models.CharField(max_length=300)
	photo = models.ImageField(blank=True) #https://wayhome25.github.io/django/2017/05/10/media-file/
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	explanation = models.StringField() # string field 같은 게 있었나?? 찾아보기

class User(models.Model): # seller buyer 구분하지 말고 걍 둘다 가능하게 해
	rating = models.IntegerField(default=0)
	userid = models.CharField(max_length=20, primary_key=True)
	pw = models.CharField(max_length=20) # min length  같은 건 js 단에서 처리하기
	username = models.CharField(max_length=100)
	phone = models.CharField(max_length=30)

class Wishlist(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	pid = models.ForeignKey(Product, on_delete=models.CASCADE)
	# 플리마켓은 필요없고
	# expire time 끝나는 순간에 보는거야.
	# 야!! 지금 이 expire time인데 wishlist에 이거 넣은놈들 다 나와바
	# 그중에 젤 큰놈? 니가 낙찰이야

# sell history
# 그냥 product에서 userid 같은 거 뽑아내고, 그 pid에서 wishlist 뽑아내면 될것같은데
# buy history는 내가 낙찰된 것만
# 낙찰안된건 알림 오고 치우기

class Category(models.Model):
	name = models.CharField(max_length=30)

# before

class History(models.Model):
	pid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateTimeField()

class Customer(models.Model):
	cid = models.CharField(max_length=20, primary_key=True)
	pw = models.CharField(max_length=20)
	birthyear = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(9999)],default=1990)
	GENDERS = (('F', 'Female'), ('M', 'Male'),('U', 'Unknown'))
	gender = models.CharField(max_length=1, default='U', choices=GENDERS)

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
