from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_home, name='vendor_home'),
    path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    path('vendor/login/', views.vendor_login, name='vendor_login'),
    path('vendor/logout/', views.vendor_logout, name='vendor_logout'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),  # New URL pattern for subcategories
    path('download_pdf/<int:category_id>/', views.download_pdf, name='download_pdf'),
]
