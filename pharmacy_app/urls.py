from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('pharmacist_dashboard/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('customers/', views.view_customers, name='customers'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('accounts/profile/', login_required(views.profile_view), name='profile'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('medicines/', views.medicines_list, name='medicines_list'),
    path('medicine/', views.available_medicines, name='medicine'),
    path('medicine_entry/', views.medicine_entry, name='medicine_entry'),
    path('medicine_update/', views.medicine_update, name='medicine_update'),
    path('medicine_entry_success/', views.medicine_entry_success, name='medicine_entry_success'),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
    path('delete/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('cart/<int:customer_id>/', views.cart, name='cart'),
    path('add_to_cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),
    path('history/',views.history, name='history'),
    path('suppliers/', views.add_supplier, name='add_supplier'),
]    
