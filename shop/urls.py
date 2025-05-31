from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('payment/', views.payment, name='payment'),
    path('payment/paypal/<int:payment_id>/', views.paypal_payment, name='paypal_payment'),
    path('payment/razorpay/<int:payment_id>/', views.razorpay_payment, name='razorpay_payment'),
    path('payment/bank-transfer/<int:payment_id>/', views.bank_transfer, name='bank_transfer'),
    path('payment/<int:payment_id>/upi/', views.upi_payment, name='upi_payment'),
    path('payment/<int:payment_id>/upi/confirm/', views.confirm_upi_payment, name='confirm_upi_payment'),
    path('payment/<int:payment_id>/cod/', views.cod_payment, name='cod_payment'),
    path('payment/<int:payment_id>/cod/confirm/', views.confirm_cod_payment, name='confirm_cod_payment'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/address/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('profile/address/<int:address_id>/set-default/', views.set_default_address, name='set_default_address'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('skincare-tips/', views.skincare_tips_view, name='skincare_tips'),
    path('makeup-trends/', views.makeup_trends_view, name='makeup_trends'),
    path('natural-beauty/', views.natural_beauty_view, name='natural_beauty'),
] 