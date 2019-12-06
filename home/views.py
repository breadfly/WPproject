from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Count

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
			number = int(form.data['number'])
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

def signup(request):
	cid = request.session.get('cid', False)
	login = 'logout'
	if cid == False: login = 'login'

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = CustomerForm()
	return render(request, 'home/signup.html', {'login':login,'form':form})

def mypage(request):
	cid = request.session.get('cid', False)
	if cid == False :
		return redirect('/login')
	else:
		what = What.objects.select_related('pid').filter(pid__cid=cid).order_by('-pid__date')
		return render(request, 'home/mypage.html', {'login':'logout','cid':cid, 'what':what})

def modifyAcc(request):
	cid = request.session.get('cid', False)
	login = 'logout'
	if cid == False: login = 'login'

	customer = Customer.objects.get(cid=cid)
	if request.method == 'POST':
		form = ModifyForm(request.POST)
		if form.is_valid():
			customer.pw = form.data['pw']
			customer.birthyear = form.data['birthyear']
			customer.gender = form.data['gender']
			customer.save()
			return redirect('/mypage')
	else:
		form = ModifyForm(initial={'birthyear':customer.birthyear, 'gender':customer.gender})
	return render(request, 'home/modifyAcc.html', {'login':login,'form':form})

def login(request):
	cid = request.session.get('cid', False)
	if cid == False: # login
		msg=''
		if request.method == 'POST':
			form = LoginForm(request.POST)
			try:
				customer = Customer.objects.get(cid=form.data['cid'], pw=form.data['pw'])
				request.session['cid'] = form.data['cid']
				return redirect('/')
			except:
				msg='로그인 정보가 올바르지 않습니다.'
				form = LoginForm()
		else:
			form = LoginForm()
		return render(request, 'home/login.html', {'login':'login','form':form, 'msg':msg})
	else:
		try:
			del request.session['cid']
		except KeyError:
			pass
		return redirect('/')

def index(request):
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