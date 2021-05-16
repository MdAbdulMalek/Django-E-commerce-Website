from django.contrib import admin

# Register your models here.

from .models import product, Contract, Order, OrderUpdate, User

admin.site.register(product)
admin.site.register(Contract)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(User)
