from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, Design, DesignImage, DesignVideo, SubCategory1, SubCategory2, SubCategory3, Package
from .forms import  *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.contrib.auth import authenticate, login
import os
from django.conf import settings
from django.templatetags.static import static  # Import the static function
import qrcode


def vendor_login(request):
    if request.method == "POST":
        form = VendorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)

            if user is not None:
                try:
                    # Fetch the vendor associated with the email
                    vendor = Vendor.objects.get(email_id=email)
                    request.session['vendor_id'] = vendor.id
                    
                    # Log in the user associated with the vendor
                    login(request, user)  # Log the user in to set request.user
                    print(f"Vendor {vendor.id} logged in successfully.")
                    print("Authenticated user after login:", request.user)
                    print("Vendor from request user:", request.user.vendor if hasattr(request.user, 'vendor') else "No vendor associated")

                    return redirect('vendor_home')
                except Vendor.DoesNotExist:
                    messages.error(request, "Vendor does not exist.")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = VendorLoginForm()

    return render(request, 'login.html', {'form': form})



def vendor_logout(request):
    logout(request)  # Log out the vendor
    return redirect('vendor_login')  # Redirect to the vendor login page


def vendor_signup(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email_id']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                messages.error(request, "This email is already in use.")
                return redirect('vendor_signup')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            package_id = request.POST.get('package')
            package = get_object_or_404(Package, id=package_id)

            vendor = Vendor(
                user=user,
                name=form.cleaned_data['name'],
                shop_name=form.cleaned_data['shop_name'],
                shop_address=form.cleaned_data['shop_address'],
                phone_number=form.cleaned_data['phone_number'],
                email_id=email,
                shop_logo=form.cleaned_data['shop_logo'],
                package=package
            )
            vendor.save()

            messages.success(request, "Vendor registered successfully! Please proceed with the payment.")
            return redirect('vendor_payment', vendor_id=vendor.id)

    else:
        form = VendorSignUpForm()

    packages = Package.objects.all()  # Fetch all packages for display
    return render(request, 'signup.html', {'form': form, 'packages': packages})


def vendor_payment(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if vendor.payment_status:
        return redirect('vendor_login')  # Redirect to login if payment is confirmed

    return render(request, 'payment.html', {'vendor': vendor, 'qr_path': vendor.package.qr_code.url})

def confirm_payment(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.payment_status = True  # Simulate payment completion
    vendor.save()
    return redirect('vendor_login')  # Redirect to login after confirming payment


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

@login_required(login_url='/vendor/login/')
def vendor_home(request):
    vendor_id = request.session.get('vendor_id')
    print(vendor_id)
    print(f"Vendor ID from session: {vendor_id}")  # Debugging line
    vendor = None

    if vendor_id:
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            print(f"Vendor found: {vendor}")  # Debugging line
            print(vendor.shop_logo.url)
            print("Loading vendor_home view")
        except Vendor.DoesNotExist:
            print("Vendor does not exist.")  # Debugging line
    else:
        print("No vendor ID found in session.")  # Debugging line

    # Fetch all categories and related designs
    categories = Category.objects.prefetch_related('design_set__images', 'design_set__videos').all()
    for i in categories:
        print(i.id)
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
    BASE_DIR = settings.BASE_DIR  # Now BASE_DIR is accessible
    category = get_object_or_404(Category, id=category_id)
    designs = category.design_set.all()
    
    vendor = request.user.vendor
    vendor_logo = vendor.shop_logo.path if vendor.shop_logo else None
    manufacturer_logo = os.path.join(settings.BASE_DIR, 'staticfiles', 'Manufacturer_logo', 'saanj_logo.jpg')
    print(manufacturer_logo)
    print(vendor_logo)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{category.name}_designs.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    def add_logos():
        print("Checking logos...")
        if os.path.exists(manufacturer_logo) and os.path.exists(vendor_logo):
            try:
                logo_image1 = ImageReader(manufacturer_logo)
                width1, height1 = logo_image1.getSize()  # Get the size
                print(f"manufacturer logo size: {width1}x{height1}")
                print("Drawing manufacturer logo...")
                p.drawImage(logo_image1, x = 30, y = 700, width= 80, height=80, preserveAspectRatio=True)
                print("manufacturer logo drawn")

                logo_image2 = ImageReader(vendor_logo)
                width, height = logo_image2.getSize()  # Get the size
                print(f"vendor logo size: {width}x{height}")
                print("Drawing vendor logo...")
                p.drawImage(logo_image2, x = 500, y = 700, width=80, height=80, preserveAspectRatio=True)
                print("Vendor logo drawn")
            except Exception as e:
                print(f"Error drawing logos: {e}")
        else:
            print("logo path is not valid")

    add_logos()


    # Add title to the PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, f"Designs for {category.name}")
    y_position = height - 120
    design_count = 0

    for design in designs:
        if y_position < 150:
            p.showPage()
            add_logos()  # Add logos on new page
            p.setFont("Helvetica-Bold", 16)
            p.drawCentredString(width / 2, height - 50, f"Designs for {category.name}")
            y_position = height - 120  # Reset vertical position for the new page
            design_count = 0

        # Calculate x_position for centering
        p.setFont("Helvetica-Bold", 12)
        text_width = p.stringWidth(design.title, "Helvetica-Bold", 12)
        x_position = (width - text_width) / 2  # Center the design title
        p.drawString(x_position, y_position, design.title)

        # Center the description and price
        p.setFont("Helvetica", 10)
        description = f"{design.description}"
        price = f"Price: {design.price}"
        
        desc_width = p.stringWidth(description, "Helvetica", 10)
        price_width = p.stringWidth(price, "Helvetica", 10)
        
        p.drawString((width - desc_width) / 2, y_position - 15, description)
        p.drawString((width - price_width) / 2, y_position - 30, price)

        # Add design images
        y_image_position = y_position - 50
        images = design.images.all()

        if images:
            x_image_position = (width - (len(images) * 120)) / 2  # Center images horizontally
            for image in images:
                image_path = image.image.path
                p.drawImage(ImageReader(image_path), x_image_position, y_image_position - 100, width=100, height=100, preserveAspectRatio=True)
                x_image_position += 120

            y_position -= 200

        if design_count % 2 == 1:
            y_position -= 10
            design_count = 0
        else:
            design_count += 1

    p.save()
    return response

@login_required(login_url='/vendor/login/')
def design_detail(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    print(design)
    vendor = request.user.vendor if hasattr(request.user, 'vendor') else None
    related_designs = Design.objects.filter(category=design.category).exclude(id=design.id)
    print(related_designs)

    for related_design in related_designs:
        print(f"Related Design ID: {related_design.id}, Title: {related_design.title}")
        for image in related_design.images.all():
            print(f"Image URL: {image.image.url}")

            
    return render(request, 'design_detail.html', {
        'design': design,
        'vendor': vendor,
        'related_designs': related_designs,
    })
