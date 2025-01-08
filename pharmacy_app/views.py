from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Customer, Pharmacist, Manager, Medicine, Order, OrderItem, Cart, CartItem, Supplier
from .forms import RegistrationForm, CustomerProfileForm, SupplierForm, ManagerProfileForm, MedicineForm, CustomAuthenticationForm


def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if Customer.objects.filter(username=username,email=email).exists():
                form.add_error(None, 'Email or username already exists.')
            else:
                user = User.objects.create_user(
                    username= username,
                    password=form.cleaned_data['password']
                )
                Customer.objects.create(user=user, email=email)
                messages.success(request, 'Account created successfully')
                return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'customer'):
                    return redirect('customer_dashboard')
                elif hasattr(user, 'pharmacist'):
                    return redirect('pharmacist_dashboard')
                elif hasattr(user, 'manager'):
                    return redirect('manager_dashboard')
                else:
                    return redirect('default_dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    return render(request, 'login.html', {'form': form})

def customer_dashboard(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    return render(request, 'customer_dashboard.html', {'customer': customer, 'orders': orders, 'customer_id': customer.id})

def history(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)
    return render(request, 'history.html', {'customer': customer, 'orders': orders, 'customer_id':customer.id})

def pharmacist_dashboard(request):
    pharmacist = request.user.pharmacist
    # orders = Order.objects.filter(customer=customer)
    return render(request, 'pharmacist_dashboard.html', {'pharmacist': pharmacist, 'pharmacist_id': pharmacist.id})

def view_customers(request):
    customers = Customer.objects.values('first_name', 'last_name', 'email', 'username')
    context = {'customers': customers}
    return render(request, 'customers.html', context)

def available_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine.html', {'medicines': medicines})

def medicine_entry(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_entry_success')
    else:
        form = MedicineForm()
    return render(request, 'medicine_entry.html', {'form': form})

def medicine_entry_success(request):
    return render(request, 'medicine_entry_success.html')

def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        medicine.delete()
        return redirect(reverse('medicine'))
    return render(request, 'delete_medicine.html', {'medicine': medicine}) 

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

def view_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers.html', {'suppliers': suppliers})

def manager_dashboard(request):
    manager = request.user.manager
    # orders = Order.objects.filter(customer=customer)
    return render(request, 'manager_dashboard.html', {'manager': manager, 'manager_id': manager.id})
    
def medicine_update(request):
    return render(request, 'medicine_update.html')   

def customer_profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')
    else:
        form = CustomerProfileForm(instance=request.user.customer)
    return render(request, 'customer_profile.html', {'form': form})

def profile_view(request):

    customer_id = request.user.id  
 
    context = {
        'customer_id': customer_id,
        'cart_items': [],  
    }
    return render(request, 'customer_dashboard.html', context)


    return render(request, 'pharmacist_dashboard.html', context)

def medicines_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicines_list.html', {'medicines': medicines})

def cart(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer)
    order_items = OrderItem.objects.filter(order__customer=customer).select_related('medicine')
    context = {
        'customer': customer,
        'orders': orders,
        'order_items': order_items,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')  

def checkout(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer, complete='True')
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'invoice.html', context)

def invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    total = sum(item.quantity * item.medicine.price for item in order.orderitem_set.all())
    return render(request, 'invoice.html', {'order': order, 'total': total})

def LogoutView(request):
    return redirect('login')



























