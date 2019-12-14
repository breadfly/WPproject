from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Count

""" ADMIN """

def adminpage(request):
	userid = request.session.get('userid', False)
	if userid != 'admin' : # 로그인 되어있으면
		return redirect('/')
	try:
		temp = User.objects.get(userid='')
		temp.delete()
	except:
		pass
	userlist = User.objects.all()
	return render(request, 'home/admin.html', {'userlist':userlist})

def userpage(request, uid=''):
	userid= uid
	isadmin = request.session.get('userid', False)
	if isadmin != 'admin' : # 로그인 되어있으면
		return redirect('/')
	try:
		user = User.objects.get(userid=userid)
	except:
		return redirect('/adminpage')

	if request.method == 'POST':
		form = ModifyForm(request.POST)
		if form.is_valid():
			if 'delete' in form.data:
				user.delete()
				del request.session['userid']
			else:
				form.save()
			return redirect('/')
	else:
		form = ModifyForm(initial={'pw':user.pw, 'phone':user.phone, 'username':user.username})
	return render(request, 'home/mypage.html', {'form':form, 'userid':userid})

def categoryadd(request):
	userid = request.session.get('userid', False)
	if userid != 'admin' : # 로그인 되어있으면
		return redirect('/')

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = CategoryForm()
	return render(request, 'home/categoryadd.html', {'form':form})

""" INDEX & ACCOUNT """

def index(request): 
	userid = request.session.get('userid', False)
	if userid != False : # 로그인 되어있으면
		return redirect('/market')
	return render(request, 'home/index.html') #안돼있으면

def register(request):
	userid = request.session.get('userid', False)
	if userid != False:#로그인상태
		return redirect('/')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request, 'home/welcome.html', {'userid':str(form.cleaned_data['userid'])})
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
				user = User.objects.get(userid=str(form.data['userid']), pw=str(form.data['pw'])) # 맞는지 비교
				request.session['userid'] = str(form.data['userid'])
				if user.userid == 'admin':
					return redirect('/adminpage')
				return redirect('/')
			except:
				msg='로그인 정보가 올바르지 않습니다.'
				form = LoginForm()
		else:
			form = LoginForm()
		return render(request, 'home/login.html', {'form':form, 'msg':msg})
	else: # login 되어있는데 이 페이지 들어왔으면? 그냥 홈으로 리다이렉트 시킬래
		return redirect('/')

def logout(request):
	userid = request.session.get('userid', False)
	if userid != False : # 로그인 되어있으면
		del request.session['userid']
	return redirect('/')

def mypage(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if request.method == 'POST':
		form = ModifyForm(request.POST)
		if form.is_valid():
			if 'delete' in form.data:
				User.objects.get(userid=userid).delete()
				del request.session['userid']
			else:
				form.save()
			return redirect('/')
	else:
		user = User.objects.get(userid=userid)
		form = ModifyForm(initial={'pw':user.pw, 'phone':user.phone, 'username':user.username})
	return render(request, 'home/mypage.html', {'form':form, 'userid':userid})

""" SELLER """

def sell(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if request.method == 'POST':
		form = SellForm(request.POST, request.FILES)
		if form.is_valid():
			if str(form.cleaned_data.get('expirechoice'))=='0':
				expire = (timezone.now() + timedelta(days=30))
			elif str(form.cleaned_data.get('expirechoice'))=='7':
				expire = (timezone.now() + timedelta(days=7))
			else:
				expire = (timezone.now() + timedelta(days=3))

			product = Product.objects.create(seller=User.objects.get(userid=userid),
				selltype=str(form.cleaned_data['selltype']),
				expire = expire,
				basic_price = int(form.cleaned_data['basic_price']),
				current_price = int(form.cleaned_data['basic_price']),
				name = str(form.cleaned_data['name']),
				place = str(form.cleaned_data['place']),
				photo = form.cleaned_data['photo'],
				category = form.cleaned_data['category'],
				explanation = str(form.cleaned_data['explanation'])
			)
			product.save()

			return redirect('/myitems')
	else:
		form = SellForm()
	return render(request, 'home/product_registration.html', {'form':form,
		'button_type':'Register', 'sell_type':''})

def editProduct(request, pid):
	try:
		product = Product.objects.get(pid=pid)
	except:
		return redirect('/')
		#raise Http404("Product does not exist")

	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	elif userid != product.seller.userid :
		return redirect('/')
	sell_type = str(product.selltype)
	form = None
	if request.method == 'POST':
		if product.selltype == 'F':
			form = EditForm1(request.POST,request.FILES)
		else :
			form = EditForm2(request.POST,request.FILES)
		
		if 'delete' in form.data:
			product.delete()
		elif 'sell' in form.data:
			sell_func(product, None)
		else:
			if form.is_valid():
				if product.selltype == 'F':
					product.basic_price = int(form.cleaned_data['basic_price'])
					product.current_price = int(form.cleaned_data['basic_price'])
				product.name = str(form.cleaned_data['name'])
				product.place = str(form.cleaned_data['place'])
				product.photo = form.cleaned_data['photo']
				product.category = form.cleaned_data['category']
				product.explanation = str(form.cleaned_data['explanation'])
				product.save()
		return redirect('/myitems')

	if product.selltype == 'F':
		form = EditForm1(initial={'basic_price':product.basic_price,
			'name':product.name, 'place':product.place, 'photo':product.photo,
			'category':product.category, 'explanation':product.explanation})
	else :
		form = EditForm2(initial={'name':product.name, 'place':product.place, 'photo':product.photo,
			'category':product.category, 'explanation':product.explanation})
	return render(request, 'home/product_registration.html', {'form':form,
		'button_type':'edit', 'sell_type':sell_type})

def sell_func(product, buyer):
	if product.selltype == 'F':
		product.buyer = buyer
		product.save()
	if product.selltype == 'A' :
		pid = product.pid
		temp = Candidate.objects.select_related('pid').filter(
			pid__pid=pid)
		if temp :
			product.buyer = temp.order_by('-price')[0].userid
			product.save()

def myitems(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	products = Product.objects.filter(seller__userid=userid).order_by('expire')
	wishnum={}
	li={}
	for product in products:
		temp = Wishlist.objects.select_related('pid').filter(pid__pid=product.pid)
		wishnum[product.pid] = len(temp)
		li[product.pid] = []
		if product.selltype == 'A':
			temp = Candidate.objects.select_related('pid').filter(pid__pid=product.pid).order_by('-price')
			for t in temp:
				li[product.pid].append(t.userid.username)
				li[product.pid].append(t.price)
	return render(request, 'home/myitems.html', {'products':products, 'history':li,
		'wishnum':wishnum})

""" BUYER """

def wishlist(request):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')

	pagetype = request.GET.get('page','')
	if pagetype == 'wish' or pagetype=='': # 내가는 아이템들과 그것을 사고 싶어하는 자들
		wishlist = Wishlist.objects.filter(userid__userid=userid,pid__expire__gte=timezone.now())
	else :  # 내가 사고 싶은 것들
		wishlist = Candidate.objects.filter(userid__userid=userid
			).select_related('pid').filter(pid__expire__gte=timezone.now())
	wishlist = wishlist.order_by('pid__expire')

	return render(request, 'home/wishlist.html', {'wishlist':wishlist})

def auction_detail(request, pid):
	msg=''
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	product = Product.objects.get(pid=pid)
	form = AuctionPurchaseForm(initial={'current_price':int(product.current_price)})

	if request.method == 'POST':
		form = AuctionPurchaseForm(request.POST)
		sellerid = str(Product.objects.get(pid=pid).seller.userid)
		if sellerid == userid:
			msg = "You cannot buy your product"
			form = AuctionPurchaseForm(initial={'current_price':int(product.current_price)})
			return render(request, 'home/auction_detail.html', {'product':product,
			'form':form,'msg':msg})
		if 'buy' in form.data:
			product = Product.objects.get(pid=pid)
			if product.current_price >= int(form.data['current_price']):
				msg = "You must bid more than current price"
				form = AuctionPurchaseForm(initial={'current_price':int(product.current_price)})
				return render(request, 'home/auction_detail.html', {'product':product,
					'form':form,'msg':msg})
			product.current_price = int(form.data['current_price'])
			candidate = Candidate.objects.create(userid=User.objects.get(userid=userid),
				pid = product, price=int(form.data['current_price']))
			product.save()
			candidate.save()
			return redirect('/myitems')
		elif 'wish' in form.data:
			wishlist = Wishlist.objects.create(userid=User.objects.get(userid=userid),
				pid = Product.objects.get(pid=pid))
			wishlist.save()
			return redirect('/wishlist')
	return render(request, 'home/auction_detail.html', {'product':product,'form':form,'msg':msg})

def market_detail(request, pid):
	msg=''
	userid = request.session.get('userid', False)
	try:
		product = Product.objects.get(pid=pid)
	except:
		return redirect('/')
	if product.expire < timezone.now() or product.buyer != None:
		return redirect('/')

	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	form = MarketPurchaseForm()
	if request.method == 'POST':
		form = MarketPurchaseForm(request.POST)
		sellerid = str(Product.objects.get(pid=pid).seller.userid)
		if sellerid == userid:
			form = MarketPurchaseForm()
			msg = "You cannot buy your product"
			return render(request, 'home/market_detail.html', {'product':product,
			'form':form,'msg':msg})
		if 'buy' in form.data:
			product = Product.objects.get(pid=pid)
			candidate = Candidate.objects.create(userid=User.objects.get(userid=userid), pid=product, price=product.current_price)
			candidate.save()
			sell_func(product, User.objects.get(userid=userid))
			return redirect('/myitems')
		elif 'wish' in form.data:
			try:
				wishlist = Wishlist.objects.create(userid=User.objects.get(userid=userid),
					pid = Product.objects.get(pid=pid))
				wishlist.save()
			except:
				pass
			return redirect('/wishlist')
	return render(request, 'home/market_detail.html', {'product':product,
	'form':form, 'msg':msg})

def detail(request, pid):
	try:
		product = Product.objects.get(pid=pid)
	except:
		return redirect('/')

	if product.expire < timezone.now() or product.buyer != None:
		return redirect('/')
	
	if product.selltype == 'F':
		return market_detail(request, pid)
	else:
		return auction_detail(request, pid)

def market(request, category=''):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if category=='':
		return redirect('/market/all/')

	categories = Category.objects.values('name').distinct()
	temp_search = {}

	# search & sort
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
		temp_search['higher'] = ''
	elif temp.isdecimal():
		higher = int(temp)
		temp_search['higher'] = higher
	else:
		return redirect('/market')

	temp_search['seller'] = seller
	temp_search['name'] = name
	temp_search['lower'] = lower

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
	
	sort=request.GET.get('sort','')
	if sort == 'lower-price':
		products = products.order_by('current_price')
	elif sort == 'lower-expire':
		products = products.order_by('expire')
	if sort == 'higher-expire':
		products = products.order_by('-expire')

	return render(request, 'home/product_market.html', {'products':products, 'categories':categories,
		'pagetype':'market', 'search':temp_search})

def auction(request, category='', search=''):
	userid = request.session.get('userid', False)
	if userid == False : # 로그인 안되어있으면
		return redirect('/login')
	if category=='':
		return redirect('/auction/all/')

	categories = Category.objects.values('name').distinct()

	# search
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

	sort=request.GET.get('sort','')
	if sort == 'lower-price':
		products = products.order_by('current_price')
	elif sort == 'lower-expire':
		products = products.order_by('expire')
	if sort == 'higher-expire':
		products = products.order_by('-expire')

	return render(request, 'home/product_market.html', {'products':products, 'categories':categories, 'pagetype':'auction'})


"""
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
"""