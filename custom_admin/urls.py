from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),

    path('categories/list_json/', views.get_categories_json, name='get_categories_json'), # JSON endpoint for categories
    path('categories/add_or_edit/', views.add_or_edit_category, name='add_or_edit_category'),
    path('categories/<int:category_id>/', views.get_category, name='get_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('categories/toggle_status/<int:category_id>/', views.toggle_category_status, name='toggle_category_status'),

    path('categories/subcategories/list_json/', views.get_subcategories_json, name='get_subcategories_json'),
    path('categories/subcategories/add_or_edit/', views.add_or_edit_subcategory, name='add_or_edit_subcategory'),
    path('categories/subcategories/<int:subcategory_id>/', views.get_subcategory, name='get_subcategory'),
    path('categories/subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('categories/subcategories/toggle_status/<int:subcategory_id>/', views.toggle_subcategory_status, name='toggle_subcategory_status'),

    path('categories/get_metal_types_json/', views.get_metal_types_json, name='get_metal_types_json'),
    path('categories/get_metal_type/<int:id>/', views.get_metal_type, name='get_metal_type'),
    path('categories/add_or_edit_metal_type/', views.add_or_edit_metal_type, name='add_or_edit_metal_type'),
    path('categories/delete_metal_type/<int:id>/', views.delete_metal_type, name='delete_metal_type'),
    path('categories/toggle_metal_status/<int:id>/', views.toggle_metal_status, name='toggle_metal_status'),

    path('categories/weight_options/list_json/', views.get_weight_options_json, name='weight_option_list_json'),
    path('categories/weight_options/<int:id>/', views.get_weight_option, name='weight_option_detail'),
    path('categories/weight_options/add_or_edit/', views.add_or_edit_weight_option, name='add_or_edit_weight_option'),
    path('categories/weight_options/delete/<int:id>/', views.delete_weight_option, name='delete_weight_option'),
    path('categories/weight_options/toggle_status/<int:id>/', views.toggle_weight_status, name='toggle_weight_status'),

    # Product management
    path('products/', views.product_list, name='product_list'),  # Display all products
    
    path('products/add_or_edit/', views.add_or_edit_product, name='add_or_edit_product'),  # Add/Edit product
    path('product/<int:product_id>/', views.get_product, name='get_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),  # Delete product
    path('products/<int:product_id>/toggle/', views.toggle_product_status, name='toggle_product_status'),  # Toggle product status
    path('products/list_json/', views.get_products_json, name='get_products_json'),
]
