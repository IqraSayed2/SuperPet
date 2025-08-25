from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','user','address_line_1','address_line_2','city','state','pincode','phoneno','created_at','updated_at','paid']

admin.site.register(Order,OrderAdmin)
