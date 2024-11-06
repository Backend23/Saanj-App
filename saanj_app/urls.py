from django.urls import path
from . import views

urlpatterns = [
    path('vendor/login/', views.vendor_login, name='vendor_login'),
    path('vendor/logout/', views.vendor_logout, name='vendor_logout'),
    path('', views.vendor_home, name='vendor_home'),
    path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    path('vendor/payment/<int:vendor_id>/', views.vendor_payment, name='vendor_payment'),
    path('vendor/confirm_payment/<int:vendor_id>/', views.confirm_payment, name='confirm_payment'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),  # New URL pattern for subcategories
    path('download_pdf/<int:category_id>/', views.download_pdf, name='download_pdf'),
    path('design/<int:design_id>/', views.design_detail, name='design_detail'),  # New URL for design detail
    path('vendor/profile/', views.vendor_profile, name='vendor_profile'),
    path('vendor/profile/edit/', views.edit_vendor_profile, name='edit_vendor_profile'),
    path('vendor/edit_logo/', views.edit_vendor_logo, name='edit_vendor_logo'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('place_order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.fake_payment, name='fake_payment'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
