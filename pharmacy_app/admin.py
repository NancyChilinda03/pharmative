from django.contrib import admin
from .models import Order, Customer, OrderItem, Manager
from .models import Medicine
from .models import Supplier
from . models import Pharmacist
from . models import Cart, CartItem


admin.site.register(Customer)

admin.site.register(Manager)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Pharmacist)

admin.site.register(Cart)

admin.site.register(CartItem)

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Medicine, MedicineAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Supplier, SupplierAdmin)





