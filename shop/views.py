from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem, NewsletterSubscriber, Payment, Address
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.contrib import messages
from django.middleware.csrf import get_token
from django.urls import reverse
from decimal import Decimal
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', None)
    show_all = request.GET.get('show_all', False)
    categories = Category.objects.all()
    
    # Get featured products (products with highest ratings or most popular)
    featured_products = Product.objects.all().order_by('-rating', '-created_at')[:6]
    
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    elif category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        if show_all:
            # Show all products when show_all is True
            products = Product.objects.all()
        else:
            # Get 2 products from each category for a diverse mix
            products = []
            for category in categories:
                category_products = Product.objects.filter(category=category)[:2]
                products.extend(category_products)
        
    return render(request, 'shop/product_list.html', {
        'products': products,
        'featured_products': featured_products,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
        'show_all': show_all
    })

@csrf_exempt
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    ).order_by('?')[:4]  # Random 4 products from same category
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login or sign up to add products to your cart.')
            return redirect('login')
        
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if not created:  # Only increment if the item already existed
            order_item.quantity += 1
            order_item.save()
        
        messages.success(request, f'{product.name} added to your cart!')
        return redirect('cart')
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    if request.method == 'POST':
        # Instead of completing the order, redirect to payment page
        return redirect('payment')
    return render(request, 'shop/cart.html', {'order': order})

@login_required
def order_summary(request):
    orders = Order.objects.filter(customer=request.user, complete=True)
    return render(request, 'shop/order_summary.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_protect
def newsletter_subscribe(request):
    if request.method == 'POST':
        # Debug message to check if we're receiving the request
        print("POST request received")
        print("CSRF Token:", request.POST.get('csrfmiddlewaretoken'))
        
        email = request.POST.get('email')
        if email:
            try:
                subscriber, created = NewsletterSubscriber.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                if created:
                    messages.success(request, 'Thank you for subscribing to our newsletter!')
                else:
                    if not subscriber.is_active:
                        subscriber.is_active = True
                        subscriber.save()
                        messages.success(request, 'Welcome back! Your subscription has been reactivated.')
                    else:
                        messages.info(request, 'You are already subscribed to our newsletter.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again later.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect('product_list')

@login_required
def payment(request):
    order = get_object_or_404(Order, customer=request.user, complete=False)
    
    # Create payment record if it doesn't exist
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.get_cart_total,
            'status': 'PENDING'
        }
    )
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method')
            return redirect('payment')
        
        # Update payment method
        payment.payment_method = payment_method
        payment.save()
        
        # Handle different payment methods
        if payment_method == 'COD':
            return redirect('cod_payment', payment_id=payment.id)
        elif payment_method == 'UPI':
            return redirect('upi_payment', payment_id=payment.id)
        else:
            messages.error(request, 'Invalid payment method selected')
            return redirect('payment')
    
    # Calculate total amount
    total_amount = order.get_cart_total
    
    return render(request, 'shop/payment_options.html', {
        'payment': payment,
        'total_amount': total_amount
    })

@login_required
def paypal_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    # Implement PayPal integration here
    return render(request, 'shop/paypal_payment.html', {'payment': payment})

@login_required
def razorpay_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    # Implement Razorpay integration here
    return render(request, 'shop/razorpay_payment.html', {'payment': payment})

@login_required
def bank_transfer(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    # Show bank account details
    return render(request, 'shop/bank_transfer.html', {'payment': payment})

@login_required
def upi_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    return render(request, 'shop/upi_payment.html', {'payment': payment})

@login_required
def confirm_upi_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        
        if transaction_id:
            # Update payment status
            payment.status = 'COMPLETED'
            payment.transaction_id = transaction_id
            payment.save()
            
            # Mark order as complete
            order = payment.order
            order.complete = True
            order.save()
            
            messages.success(request, 'Payment confirmed! Your order has been placed.')
            return redirect('order_summary')
        else:
            messages.error(request, 'Please provide a transaction ID.')
    
    return redirect('upi_payment', payment_id=payment_id)

@login_required
def cod_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    if payment.status == 'completed':
        messages.warning(request, 'This payment has already been processed.')
        return redirect('order_detail', order_id=payment.order.id)
    
    return render(request, 'shop/cod_payment.html', {'payment': payment})

@login_required
def confirm_cod_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__customer=request.user)
    if payment.status == 'completed':
        messages.warning(request, 'This payment has already been processed.')
        return redirect('order_summary')
    
    if request.method == 'POST':
        payment.status = 'pending'  # Set to pending until delivery is confirmed
        payment.payment_method = 'cod'
        payment.save()
        
        # Update order status
        order = payment.order
        order.status = 'processing'
        order.save()
        
        messages.success(request, 'Your order has been placed successfully! You will receive a confirmation email shortly.')
        return redirect('order_summary')
    
    return redirect('cod_payment', payment_id=payment_id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'shop/order_detail.html', {
        'order': order,
        'items': order.orderitem_set.all(),
        'payment': order.payment_set.first() if hasattr(order, 'payment_set') else None
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
            messages.success(request, 'Item removed from cart.')
            return redirect('cart')
    
    item.save()
    messages.success(request, 'Cart updated successfully.')
    return redirect('cart')

@login_required
def user_profile(request):
    user = request.user
    addresses = user.addresses.all()
    orders = Order.objects.filter(customer=user, complete=True).order_by('-date_ordered')
    
    if request.method == 'POST':
        # Handle address form submission
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        is_default = request.POST.get('is_default') == 'on'
        
        if street_address and city and state and zip_code:
            # If this is set as default, unset other default addresses
            if is_default:
                user.addresses.filter(is_default=True).update(is_default=False)
            
            Address.objects.create(
                user=user,
                street_address=street_address,
                apartment_address=apartment_address,
                city=city,
                state=state,
                zip_code=zip_code,
                is_default=is_default
            )
            messages.success(request, 'Address added successfully!')
            return redirect('user_profile')
    
    return render(request, 'shop/user_profile.html', {
        'user': user,
        'addresses': addresses,
        'orders': orders
    })

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('user_profile')

@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    # Unset other default addresses
    request.user.addresses.filter(is_default=True).update(is_default=False)
    # Set this address as default
    address.is_default = True
    address.save()
    messages.success(request, 'Default address updated successfully!')
    return redirect('user_profile')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('product_list')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def contact_view(request):
    return render(request, 'shop/contact.html')

# Add views for beauty tips sections
def skincare_tips_view(request):
    return render(request, 'shop/skincare_tips.html', {'title': 'Skincare Essentials'})

def makeup_trends_view(request):
    return render(request, 'shop/makeup_trends.html', {'title': 'Makeup Trends'})

def natural_beauty_view(request):
    return render(request, 'shop/natural_beauty.html', {'title': 'Natural Beauty'})
