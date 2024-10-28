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
]
