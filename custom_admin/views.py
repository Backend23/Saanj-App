# views.py in custom_admin

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from saanj_app.models import *
from saanj_app.forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Admin Login View
def admin_login(request):
    print("admin_login view called")  # Check if the function is called
    print(request.method)
    if request.method == 'POST':
        print("POST request received")  # Check if POST request is received
        form = AdminLoginForm(request.POST)
        print('form received')
        if form.is_valid():
            print('valid form')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None and user.is_staff:
                print('logged in')
                login(request, user)
                return redirect('custom_admin_dashboard')
            else:
                form.add_error(None, 'Invalid credentials or user is not an admin.')
    else:
        print("GET request received")  # Check if GET request is received
        form = AdminLoginForm()
    return render(request, 'custom_admin/login.html', {'form': form})


# Admin Dashboard View
def custom_admin_dashboard(request):
    return render(request, 'custom_admin/dashboard.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('admin_login')

# Design Views
class DesignListView(ListView):
    model = Design
    template_name = 'custom_admin/design_list.html'
    context_object_name = 'designs'

class DesignDetailView(DetailView):
    model = Design
    template_name = 'custom_admin/design_detail.html'
    context_object_name = 'design'

class DesignCreateView(CreateView):
    model = Design
    form_class = DesignUploadForm
    template_name = 'custom_admin/design_form.html'

class DesignUpdateView(UpdateView):
    model = Design
    form_class = DesignUploadForm
    template_name = 'custom_admin/design_form.html'

class DesignDeleteView(DeleteView):
    model = Design
    template_name = 'custom_admin/design_confirm_delete.html'
    success_url = '/custom-admin/designs/'

# Vendor Views
class VendorListView(ListView):
    model = Vendor
    template_name = 'custom_admin/vendor_list.html'
    context_object_name = 'vendors'

class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'custom_admin/vendor_detail.html'
    context_object_name = 'vendor'

class VendorCreateView(CreateView):
    model = Vendor
    form_class = VendorSignUpForm
    template_name = 'custom_admin/vendor_form.html'

class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = VendorSignUpForm
    template_name = 'custom_admin/vendor_form.html'

class VendorDeleteView(DeleteView):
    model = Vendor
    template_name = 'custom_admin/vendor_confirm_delete.html'
    success_url = '/custom-admin/vendors/'

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'custom_admin/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'custom_admin/category_form.html'

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'custom_admin/category_form.html'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'custom_admin/category_confirm_delete.html'
    success_url = '/custom-admin/categories/'

# SubCategory Views
class SubCategory1ListView(ListView):
    model = SubCategory1
    template_name = 'custom_admin/subcategory1_list.html'
    context_object_name = 'subcategory1s'

class SubCategory1CreateView(CreateView):
    model = SubCategory1
    form_class = SubCategory1Form
    template_name = 'custom_admin/subcategory1_form.html'

class SubCategory1UpdateView(UpdateView):
    model = SubCategory1
    form_class = SubCategory1Form
    template_name = 'custom_admin/subcategory1_form.html'

class SubCategory1DeleteView(DeleteView):
    model = SubCategory1
    template_name = 'custom_admin/subcategory1_confirm_delete.html'
    success_url = '/custom-admin/subcategories1/'

# SubCategory2 Views
class SubCategory2ListView(ListView):
    model = SubCategory2
    template_name = 'custom_admin/subcategory2_list.html'
    context_object_name = 'subcategory2s'

class SubCategory2CreateView(CreateView):
    model = SubCategory2
    form_class = SubCategory2Form
    template_name = 'custom_admin/subcategory2_form.html'

class SubCategory2UpdateView(UpdateView):
    model = SubCategory2
    form_class = SubCategory2Form
    template_name = 'custom_admin/subcategory2_form.html'

class SubCategory2DeleteView(DeleteView):
    model = SubCategory2
    template_name = 'custom_admin/subcategory2_confirm_delete.html'
    success_url = '/custom-admin/subcategories2/'

# SubCategory3 Views
class SubCategory3ListView(ListView):
    model = SubCategory3
    template_name = 'custom_admin/subcategory3_list.html'
    context_object_name = 'subcategory3s'

class SubCategory3CreateView(CreateView):
    model = SubCategory3
    form_class = SubCategory3Form
    template_name = 'custom_admin/subcategory3_form.html'

class SubCategory3UpdateView(UpdateView):
    model = SubCategory3
    form_class = SubCategory3Form
    template_name = 'custom_admin/subcategory3_form.html'

class SubCategory3DeleteView(DeleteView):
    model = SubCategory3
    template_name = 'custom_admin/subcategory3_confirm_delete.html'
    success_url = '/custom-admin/subcategories3/'

# Address Views
class AddressListView(ListView):
    model = Address
    template_name = 'custom_admin/address_list.html'
    context_object_name = 'addresses'

class AddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'custom_admin/address_form.html'

class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'custom_admin/address_form.html'

class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'custom_admin/address_confirm_delete.html'
    success_url = '/custom-admin/addresses/'

