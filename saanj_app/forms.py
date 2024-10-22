from django import forms
from .models import *
from django.forms import modelformset_factory

class DesignUploadForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['title', 'description', 'category', 'price', 'subcategory1', 'subcategory2', 'subcategory3']  # Include image and video fields]

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Invalid file type. Please upload a PNG or JPEG image.")
        video = self.cleaned_data.get('videp')
        if video and not video.name.endswith(('.mp4, .mov, .mkv')):
            raise forms.ValidationError('Invalid file type. Please upload a mp4 or mkv image. ')
        return image

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

