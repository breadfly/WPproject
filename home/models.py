import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 


class Category(models.Model):
	name = models.CharField(max_length=30)

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

class History(models.Model):
	pid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateTimeField()

class What(models.Model):
	pid = models.ForeignKey(History, on_delete=models.CASCADE)
	isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
	num = models.IntegerField(default=1)
