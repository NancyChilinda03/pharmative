from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
import datetime

    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)  
    username = models.CharField(max_length=30)  
    password = models.CharField(max_length=128)  


    def __str__(self):
         return self.user.username


class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(max_length=100, unique=True)  
    password = models.CharField(default= '', max_length=128)        
    employee_id = models.CharField(max_length=20, default= '')

    def __str__(self):
        return self.user.username      



class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    employee_id = models.CharField(max_length=20)
    password = models.CharField(default= '', max_length=120)

    def __str__(self):
        return self.user.username
    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(default='')

    def __str__(self):
        return self.name    

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    minimum_quantity = models.IntegerField(default=0)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    expiry_date = models.DateField(default='2024-05-07')

    def __str__(self):
        return self.name

    
    def is_out_of_stock(self):
        return self.quantity < self.minimum_quantity

    def is_expired(self):
        return self.expiry_date < date.today()
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine.name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.customer.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.medicine.name}"



