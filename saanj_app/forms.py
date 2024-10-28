from django import forms
from .models import *
from django.forms import modelformset_factory
from django.contrib.auth.forms import AuthenticationForm

class DesignUploadForm(forms.ModelForm):

    package = forms.ModelChoiceField(
        queryset=Package.objects.all(),
        required=True,
        help_text="Select the package this design belongs to."
    )
    class Meta:
        model = Design
        fields = ['title', 'description', 'category', 'price', 'subcategory1', 'subcategory2', 'subcategory3', 'package']  # Include image and video fields]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']  # Ensure 'parent' exists in the model


class SubCategory1Form(forms.ModelForm):
    class Meta:
        model = SubCategory1
        fields = ['name', 'category'] 

class SubCategory2Form(forms.ModelForm):
    class Meta:
        model = SubCategory2
        fields = ['name', 'subcategory1'] 

class SubCategory3Form(forms.ModelForm):
    class Meta:
        model = SubCategory3
        fields = ['name', 'subcategory2'] 



class VendorSignUpForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'shop_name', 'shop_address', 'phone_number', 'email_id', 'password', 'shop_logo']
        widgets = {
            'password': forms.PasswordInput(),
        }


class VendorLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput())

class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
