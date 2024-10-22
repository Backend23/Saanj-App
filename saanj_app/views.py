from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, Design, DesignImage, DesignVideo, SubCategory1, SubCategory2, SubCategory3
from .forms import  *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.contrib.auth import authenticate, login



# Display Category Details
def vendor_signup(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the cleaned data from the form
            email = form.cleaned_data['email_id']
            password = form.cleaned_data['password']  # Get the raw password

            # Check if the email is already in use
            if User.objects.filter(username=email).exists():
                messages.error(request, "This email is already in use.")
                return redirect('vendor_signup')

            # Create the user object (this handles user authentication)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password  # Set the password directly, Django will hash it
            )

            # Create the Vendor instance
            vendor = Vendor(
                user=user,  # Associate the user with the vendor
                name=form.cleaned_data['name'],
                shop_name=form.cleaned_data['shop_name'],
                shop_address=form.cleaned_data['shop_address'],
                phone_number=form.cleaned_data['phone_number'],
                email_id=email,
                shop_logo=form.cleaned_data['shop_logo']
            )
            vendor.save()  # Save the vendor instance
            messages.success(request, "Vendor registered successfully!")
            return redirect('vendor_login')
    else:
        form = VendorSignUpForm()
    return render(request, 'signup.html', {'form': form})

def vendor_login(request):
    if request.method == "POST":
        form = VendorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                vendor = Vendor.objects.get(email_id=email)
                if vendor.user.check_password(password):  # Use Django's built-in method
                    request.session['vendor_id'] = vendor.id
                    print(f"Vendor {vendor.id} logged in successfully.")  # Debug line
                    return redirect('vendor_home')
                else:
                    messages.error(request, "Invalid email or password.")
            except Vendor.DoesNotExist:
                messages.error(request, "Invalid email or password.")
        return redirect('vendor_login')
    else:
        form = VendorLoginForm()

    return render(request, 'login.html', {'form': form})

def vendor_logout(request):
    logout(request)  # Use Django's built-in logout function
    return redirect('vendor_home')  # Redirect to the vendor home page after logging out

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    
    # Fetch Level 1 subcategories
    subcategories_level1 = SubCategory1.objects.filter(category_id=category_id).values('id', 'name')

    # Fetch Level 2 subcategories for each Level 1 subcategory
    subcategories_level2 = SubCategory2.objects.filter(
        subcategory_level1__category_id=category_id
    ).values('id', 'name', 'subcategory_level1_id')

    # Fetch Level 3 subcategories for each Level 2 subcategory
    subcategories_level3 = SubCategory3.objects.filter(
        subcategory_level2__subcategory_level1__category_id=category_id
    ).values('id', 'name', 'subcategory_level2_id')

    # Organizing the data into a structured response
    response_data = {
        'level1': list(subcategories_level1),
        'level2': list(subcategories_level2),
        'level3': list(subcategories_level3),
    }
    
    return JsonResponse(response_data, safe=False)

def vendor_home(request):
    vendor_id = request.session.get('vendor_id')
    print(vendor_id)
    print(f"Vendor ID from session: {vendor_id}")  # Debugging line
    vendor = None

    if vendor_id:
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            print(f"Vendor found: {vendor}")  # Debugging line
        except Vendor.DoesNotExist:
            print("Vendor does not exist.")  # Debugging line
    else:
        print("No vendor ID found in session.")  # Debugging line

    # Fetch all categories and related designs
    categories = Category.objects.prefetch_related('design_set').all()
    
    # Fetch all subcategories
    subcategories1 = SubCategory1.objects.all()
    subcategories2 = SubCategory2.objects.all()
    subcategories3 = SubCategory3.objects.all()
    
    return render(request, 'home.html', {
        'categories': categories,
        'vendor': vendor,
        'subcategories1': subcategories1,
        'subcategories2': subcategories2,
        'subcategories3': subcategories3,
    })


@login_required(login_url='/vendor/login/')
def download_pdf(request, category_id):
    print('Request User:', request.user)
    print('User is authenticated:', request.user.is_authenticated)
    print('Has Vendor:', hasattr(request.user, 'vendor'))
    print('Vendor ID:', request.session.get('vendor_id'))  # Print vendor ID from session

    # Get the category and associated designs
    category = get_object_or_404(Category, id=category_id)
    designs = category.design_set.all()

    # Check if the logged-in user is a vendor
    if not hasattr(request.user, 'vendor'):
        messages.error(request, "Error: You must be a vendor to download the PDF.")
        return redirect('vendor_login')  # Redirect to login if not a vendor

    vendor = request.user.vendor
    vendor_logo = vendor.shop_logo.path if vendor.shop_logo else None

    # Assuming manufacturer details are related to the category
    manufacturer_logo = category.manufacturer.logo.path if hasattr(category, 'manufacturer') and category.manufacturer.logo else None

    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{category.name}_designs.pdf"'

    # Create the PDF object
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add logos if available
    if manufacturer_logo:
        p.drawImage(ImageReader(manufacturer_logo), 40, height - 80, width=100, preserveAspectRatio=True)
    if vendor_logo:
        p.drawImage(ImageReader(vendor_logo), width - 140, height - 80, width=100, preserveAspectRatio=True)

    # Add title and designs to PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, f"Designs for {category.name}")
    y_position = height - 120

    for design in designs:
        if y_position < 100:  # Add a new page if space is insufficient
            p.showPage()
            y_position = height - 80

        # Display design details
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y_position, design.title)
        p.setFont("Helvetica", 10)
        p.drawString(40, y_position - 15, f"Description: {design.description}")
        p.drawString(40, y_position - 30, f"Price: {design.price}")

        # Add design images
        images = design.images.all()
        if images:
            image_path = images[0].image.path  # Display the first image
            p.drawImage(ImageReader(image_path), 40, y_position - 130, width=200, height=100, preserveAspectRatio=True)
            y_position -= 150

        y_position -= 50

    # Close the PDF object and return the response
    p.showPage()
    p.save()
    return response
