from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Count

def wishlist(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	wishlist = Wishlist.objects.filter(userid__userid=userid,pid__expire__gte=timezone.now())
	return render(request, 'home/wishlist.html', {'type':'wishlist','wishlist':wishlist})

def auction_detail(request, pid):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	form = AuctionPurchaseForm()
	if request.method == 'POST':
		form = AuctionPurchaseForm(request.POST)
		if 'buy' in form.data:
			product = Product.objects.get(pid=pid)
			if product.current_price < int(form.data['current_price']):
				product.current_price = form.data['current_price']
			candidate = Candidate.objects.create(userid=User.objects.get(userid=userid),
				pid = product, price=form.data['current_price'])
			candidate.save()
			return redirect('/myitems')
		elif 'wish' in form.data:
			wishlist = Wishlist.objects.create(userid=User.objects.get(userid=userid),
				pid = Product.objects.get(pid=pid))
			wishlist.save()
			return redirect('/wishlist')
	return render(request, 'home/auction_detail.html', {'form':form})

def market_detail(request, pid):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	form = MarketPurchaseForm()
	if request.method == 'POST':
		form = MarketPurchaseForm(request.POST)
		if 'buy' in form.data:
			product = Product.objects.get(pid=pid)
			candidate = Candidate.objects.create(userid=User.objects.get(userid=userid), pid=product, price=product.current_price)
			candidate.save()
			return redirect('/myitems')
		elif 'wish' in form.data:
			try:
				wishlist = Wishlist.objects.create(userid=User.objects.get(userid=userid),
					pid = Product.objects.get(pid=pid))
				wishlist.save()
			except:
				pass
			return redirect('/wishlist')
	return render(request, 'home/market_detail.html', {'form':form})

def detail(request, pid):
	try:
		product = Product.objects.get(pid=pid)
	except:
		raise Http404("Product does not exist")
	if product.selltype == 'F':
		return market_detail(request, pid)
	else:
		return auction_detail(request, pid)

def logout(request):
	userid = request.session.get('userid', False)
	if userid != False : # 로그인 되어있으면
		del request.session['userid']
	return redirect('/')

def myitems(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	myitems = Product.objects.filter(buyer__userid=userid)
	return render(request, 'home/myitems.html', {'products':myitems})

def market(request, category=''):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if category=='':
		return redirect('/market/all/')

	categories = Category.objects.values('name').distinct()

	# search
	if request.method == 'GET':
		seller = str(request.GET.get('seller', ''))
		name = str(request.GET.get('name', ''))
		temp = request.GET.get('lower', '')
		if temp == '':
			lower = 0
		elif temp.isdecimal():
			lower = int(temp)
		else:
			return redirect('/market')
		temp = request.GET.get('higher', '')
		if temp == '':
			higher = 2147483647
		elif temp.isdecimal():
			higher = int(temp)
		else:
			return redirect('/market')

		if category == 'all':
			products = Product.objects.filter(selltype='F',
				buyer=None, expire__gte=timezone.now(),
				name__icontains=name,
				seller__username__icontains=seller,
				current_price__gte=lower,
				current_price__lte=higher)
		else :
			products = Product.objects.filter(category__name=category,
				selltype='F', buyer=None, expire__gte=timezone.now(),
				name__icontains=name,
				seller__username__icontains=seller,
				current_price__gte=lower,
				current_price__lte=higher)
	else:
		if category == 'all':
			products = Product.objects.filter(selltype='F',
				buyer=None, expire__gte=timezone.now())
		else :
			products = Product.objects.filter(category__name=category,
				selltype='F', buyer=None, expire__gte=timezone.now())

	return render(request, 'home/product_market.html', {'products':products, 'categories':categories})

def auction(request, category='', search=''):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if category=='':
		return redirect('/auction/all/')

	categories = Category.objects.values('name').distinct()

	# search
	if request.method == 'GET':
		seller = str(request.GET.get('seller', ''))
		name = str(request.GET.get('name', ''))
		temp = request.GET.get('lower', '')
		if temp == '':
			lower = 0
		elif temp.isdecimal():
			lower = int(temp)
		else:
			return redirect('/auction')
		temp = request.GET.get('higher', '')
		if temp == '':
			higher = 2147483647
		elif temp.isdecimal():
			higher = int(temp)
		else:
			return redirect('/auction')

		if category == 'all':
			products = Product.objects.filter(selltype='A',
				buyer=None, expire__gte=timezone.now(),
				name__icontains=name,
				seller__username__icontains=seller,
				current_price__gte=lower,
				current_price__lte=higher)
		else :
			products = Product.objects.filter(category__name=category,
				selltype='A', buyer=None, expire__gte=timezone.now(),
				name__icontains=name,
				seller__username__icontains=seller,
				current_price__gte=lower,
				current_price__lte=higher)
	else:
		if category == 'all':
			products = Product.objects.filter(selltype='A',
				buyer=None, expire__gte=timezone.now())
		else :
			products = Product.objects.filter(category__name=category,
				selltype='A', buyer=None, expire__gte=timezone.now())

	return render(request, 'home/product_market.html', {'products':products, 'categories':categories})

def sell(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if request.method == 'POST':
		form = SellForm(request.POST, request.FILES)
		if form.is_valid():
			product = Product.objects.create(seller=User.objects.get(userid=userid),
				selltype=form.cleaned_data['selltype'],
				expire = form.cleaned_data['expire'],
				basic_price = form.cleaned_data['basic_price'],
				current_price = form.cleaned_data['basic_price'],
				name = form.cleaned_data['name'],
				place = form.cleaned_data['place'],
				photo = form.cleaned_data['photo'],
				category = form.cleaned_data['category'],
				explanation = form.cleaned_data['explanation']
			)
			product.save()

			return redirect('/myitems')
	else:
		form = SellForm()
	return render(request, 'home/product_registration.html', {'form':form})

def register(request):
	userid = request.session.get('userid', False)
	if userid != False:#로그인상태
		return redirect('/')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'home/welcome.html', {'userid':form.cleaned_data['userid']})
	else:
		form = RegisterForm()
	return render(request, 'home/register.html', {'form':form})

def login(request):
	userid = request.session.get('userid', False)
	if userid == False: # login안되어있으면
		msg=''
		if request.method == 'POST':
			form = LoginForm(request.POST)
			try:
				user = User.objects.get(userid=form.data['userid'], pw=form.data['pw']) # 맞는지 비교
				request.session['userid'] = form.data['userid']
				return redirect('/')
			except:
				msg='로그인 정보가 올바르지 않습니다.'
				form = LoginForm()
		else:
			form = LoginForm()
		return render(request, 'home/login.html', {'form':form, 'msg':msg})
	else: # login 되어있는데 이 페이지 들어왔으면? 그냥 홈으로 리다이렉트 시킬래
		return redirect('/')
		"""try:
			del request.session['cid']
		except KeyError:
			pass"""

def index(request): # 로고에 animate.css 넣어도 이쁘겠군.. 나중에 해봐야지
	userid = request.session.get('userid', False)
	if userid != False : # 로그인 되어있으면
		return redirect('/market')
	return render(request, 'home/index.html') #안돼있으면

	"""
	cid = request.session.get('cid', False)
	rec = recommend(cid)
	if cid != False:
		g = Customer.objects.get(cid=cid).gender
		if g == 'F':
			gender = '여자'
		elif g == 'M':
			gender = '남자'
		else: 
			gender = '유저'
		return render(request, 'home/index.html', {'login':'logout','cid':cid, 'gender':gender, 'recommend':rec})
	else:
		return render(request, 'home/index.html', {'login':'login','cid':None, 'recommend':rec})
	"""

#############################

def purchase(request):
	cid = request.session.get('cid',False)
	if cid == False :
		return redirect('/login')
	if request.method == 'POST':
		cart = Cart.objects.filter(cid=cid)
		history = History(cid_id=cid, date=datetime.datetime.now())
		history.save()
		pid = history.pid
		for book in cart:
			what = What(pid_id=pid, isbn=book.isbn, num=book.num)
			what.save()
		cart.delete()
	else :
		return redirect('/')
	return render(request, 'home/purchase.html', {'login':'logout','pid':pid})

def cart(request):
	cid = request.session.get('cid', False)
	if cid == False :
		return redirect('/login')

	if request.method == 'POST': # 아이템 제거 명령
		keys = request.POST.keys()
		for key in keys :
			if key == 'csrfmiddlewaretoken' : continue
			Cart.objects.get(cid=cid, isbn=key).delete()

	cart = Cart.objects.filter(cid=cid).select_related('isbn')
	price = 0
	for obj in cart:
		price += obj.num * obj.isbn.price
	return render(request, 'home/cart.html', {'login':'logout','cart':cart, 'cid':cid, 'price':price})

def bookList(request,category=''):
	login = 'logout'
	cid = request.session.get('cid', False)
	if cid == False: login = 'login'

	categories = Category.objects.values('name').distinct()
	books = None

	sort=request.GET.get('sort','')
	if sort == 'lower-price':
		if category =='': books = Book.objects.all()
		else : books = Book.objects.filter(category__name=category)
		books = books.order_by('price')
	elif sort == 'higher-price':
		if category =='': books = Book.objects.all()
		else : books = Book.objects.filter(category__name=category)
		books = books.order_by('-price')
	else :
		if category =='': books = Book.objects.all()
		else : books = Book.objects.filter(category__name=category)
		books = books.order_by('-price')
	return render(request, 'home/books.html', {'login':login,'books':books,'category':categories})
"""
def detail(request, category, isbn):
	try:
		book = Book.objects.get(isbn=isbn,category__name=category)
	except :
		raise Http404("Book does not exist")
	form = AddCartForm()
	cid = request.session.get('cid', False)
	if request.method == 'POST':
		if cid == False :
			return redirect('/login')
		else : 
			form = AddCartForm(request.POST)
			number = int(form.cleaned_data['number'])
			try :
				already = Cart.objects.get(cid_id=cid, isbn_id=isbn)
				already.num += number
				already.save()
			except:
				cart = Cart(cid_id=cid, isbn_id=isbn, num=number)
				cart.save()
			messages.success(request, '책이 카트에 추가되었습니다.')
	else:
		form = AddCartForm()
	login = 'logout'
	if cid == False: login = 'login'
	categories = Category.objects.values('name').distinct()
	return render(request, 'home/detail.html', {'login':login, 'book':book,'form':form,'category':categories})
"""
"""def mypage(request):

	cid = request.session.get('cid', False)
	if cid == False :
		return redirect('/login')
	else:
		what = What.objects.select_related('pid').filter(pid__cid=cid).order_by('-pid__date')
		return render(request, 'home/mypage.html', {'login':'logout','cid':cid, 'what':what})
"""
def mypage(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	user = User.objects.get(userid=userid)
	if request.method == 'POST':
		form = ModifyForm(request.POST)
		if form.is_valid():
			user.pw = form.cleaned_data['pw']
			user.username = form.cleaned_data['username']
			user.phone = form.cleaned_data['phone']
			user.save()
			return redirect('/')
	else:
		form = ModifyForm(initial={'phone':user.phone, 'username':user.username})
	return render(request, 'home/mypage.html', {'form':form})


def modifyAcc(request):
	cid = request.session.get('cid', False)
	login = 'logout'
	if cid == False: login = 'login'

	customer = Customer.objects.get(cid=cid)
	if request.method == 'POST':
		form = ModifyForm(request.POST)
		if form.is_valid():
			customer.pw = form.cleaned_data['pw']
			customer.birthyear = form.cleaned_data['birthyear']
			customer.gender = form.cleaned_data['gender']
			customer.save()
			return redirect('/mypage')
	else:
		form = ModifyForm(initial={'birthyear':customer.birthyear, 'gender':customer.gender})
	return render(request, 'home/modifyAcc.html', {'login':login,'form':form})

def recommend(cid):
	if cid == False:
		what = What.objects.all()
		bestList = what.values('isbn').annotate(total=Count('isbn')).order_by('-total')[:3]
	else:
		customer = Customer.objects.get(cid=cid)
		birth = customer.birthyear
		gender = customer.gender
		print(birth)
		if customer.gender == "U":
			what = What.objects.select_related('pid__cid').filter(pid__cid__birthyear__gte=birth-5, pid__cid__birthyear__lte=birth+5)
		else :
			what = What.objects.select_related('pid__cid').filter(pid__cid__gender=gender, pid__cid__birthyear__gte=birth-5, pid__cid__birthyear__lte=birth+5)
		# what ; 비슷한 사람들이 산 책
		bestList = what.values('isbn').annotate(total=Count('isbn')).order_by('-total')[:3]
	bookList = []
	for best in bestList:
		bookList.append(Book.objects.get(isbn=best['isbn']))
	return bookList