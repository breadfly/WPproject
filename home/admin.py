from django.contrib import admin
from home.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Category)