# urls.py in custom_admin

from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='admin_logout'),
    path('dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),

    # Design URLs
    path('designs/', views.DesignListView.as_view(), name='design_list'),
    path('design/<int:pk>/', views.DesignDetailView.as_view(), name='design_detail'),
    path('design/create/', views.DesignCreateView.as_view(), name='design_create'),
    path('design/update/<int:pk>/', views.DesignUpdateView.as_view(), name='design_update'),
    path('design/delete/<int:pk>/', views.DesignDeleteView.as_view(), name='design_delete'),

    # Vendor URLs
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendor/<int:pk>/', views.VendorDetailView.as_view(), name='vendor_detail'),
    path('vendor/create/', views.VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', views.VendorUpdateView.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', views.VendorDeleteView.as_view(), name='vendor_delete'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # SubCategory1 URLs
    path('subcategories1/', views.SubCategory1ListView.as_view(), name='subcategory1_list'),
    path('subcategory1/create/', views.SubCategory1CreateView.as_view(), name='subcategory1_create'),
    path('subcategory1/update/<int:pk>/', views.SubCategory1UpdateView.as_view(), name='subcategory1_update'),
    path('subcategory1/delete/<int:pk>/', views.SubCategory1DeleteView.as_view(), name='subcategory1_delete'),

    # SubCategory2 URLs
    path('subcategories2/', views.SubCategory2ListView.as_view(), name='subcategory2_list'),
    path('subcategory2/create/', views.SubCategory2CreateView.as_view(), name='subcategory2_create'),
    path('subcategory2/update/<int:pk>/', views.SubCategory2UpdateView.as_view(), name='subcategory2_update'),
    path('subcategory2/delete/<int:pk>/', views.SubCategory2DeleteView.as_view(), name='subcategory2_delete'),

    # SubCategory3 URLs
    path('subcategories3/', views.SubCategory3ListView.as_view(), name='subcategory3_list'),
    path('subcategory3/create/', views.SubCategory3CreateView.as_view(), name='subcategory3_create'),
    path('subcategory3/update/<int:pk>/', views.SubCategory3UpdateView.as_view(), name='subcategory3_update'),
    path('subcategory3/delete/<int:pk>/', views.SubCategory3DeleteView.as_view(), name='subcategory3_delete'),

    # Address URLs
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/update/<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='address_delete'),
]
