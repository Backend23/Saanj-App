from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import *
from .forms import  *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.contrib.auth import authenticate, login
import os
from django.db.models import Q
from django.conf import settings
from django.templatetags.static import static  # Import the static function
import qrcode
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.db.models import Prefetch


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

from collections import defaultdict
from django.db.models import Prefetch

from django.db.models import Q

@login_required(login_url='/vendor/login/')
def vendor_home(request):
    vendor_id = request.session.get('vendor_id')
    print(f"Vendor ID from session: {vendor_id}")  # Debugging line
    vendor = None

    if vendor_id:
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            print(f"Vendor found: {vendor}")  # Debugging line
        except Vendor.DoesNotExist:
            print("Vendor does not exist.")  # Debugging line
            return redirect('/vendor/login/')
    else:
        print("No vendor ID found in session.")  # Debugging line
        return redirect('/vendor/login/')

    # Ensure the vendor is logged in and has a package
    if vendor and vendor.package:
        # Retrieve vendor's package level
        vendor_package_level = vendor.package.level
        print('Vendor package level:', vendor_package_level)

        # Filter designs based on the vendor's package level, excluding any without packages
        allowed_designs = Design.objects.filter(
            Q(package__level__lte=vendor_package_level)
        ).select_related('category', 'package')  # Select related fields to avoid extra DB queries
        print('Filtered designs based on package level:')

        # Organize designs by category
        designs_by_category = defaultdict(list)
        for design in allowed_designs:
            designs_by_category[design.category_id].append(design)
            print(f"Design: {design.title}")
            for image in design.images.all():
                print(f"Image URL: {image.image.url}")

        # Fetch only the categories with allowed designs
        categories = Category.objects.filter(id__in=designs_by_category.keys())

        # Attach designs to categories
        categories_with_designs = []
        for category in categories:
            print(f"Category: {category.name}, Designs: {designs_by_category.get(category.id, [])}")
            category.designs = designs_by_category.get(category.id, [])
            print(category.designs)
            categories_with_designs.append(category)
        print(f"Categories with designs: {categories_with_designs}")
    else:
        categories_with_designs = []  # No categories if no vendor or package
    
    # Fetch all subcategories
    subcategories1 = SubCategory1.objects.all()
    subcategories2 = SubCategory2.objects.all()
    subcategories3 = SubCategory3.objects.all()
    
    return render(request, 'home.html', {
        'allowed_designs': allowed_designs,  # Pass designs directly
        'categories': categories_with_designs,
        'vendor': vendor,
        'subcategories1': subcategories1,
        'subcategories2': subcategories2,
        'subcategories3': subcategories3,
    })





@login_required(login_url='/vendor/login/')
def download_pdf(request, category_id):
    BASE_DIR = settings.BASE_DIR
    category = get_object_or_404(Category, id=category_id)

    vendor = request.user.vendor
    vendor_package_level = vendor.package.level if vendor.package else None
    
    # Filter designs based on vendor's package level
    designs = category.design_set.filter(
        Q(package__level__lte=vendor_package_level)
    ).select_related('package')

    vendor_logo = vendor.shop_logo.path if vendor.shop_logo else None
    manufacturer_logo = os.path.join(settings.BASE_DIR, 'staticfiles', 'Manufacturer_logo', 'saanj_logo.jpg')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{category.name}_designs.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    def add_logos():
        if os.path.exists(manufacturer_logo) and os.path.exists(vendor_logo):
            try:
                logo_image1 = ImageReader(manufacturer_logo)
                p.drawImage(logo_image1, x=30, y=700, width=80, height=80, preserveAspectRatio=True)

                logo_image2 = ImageReader(vendor_logo)
                p.drawImage(logo_image2, x=500, y=700, width=80, height=80, preserveAspectRatio=True)
            except Exception as e:
                print(f"Error drawing logos: {e}")

    add_logos()

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, f"Designs for {category.name}")
    y_position = height - 120
    design_count = 0

    for design in designs:
        if y_position < 150:
            p.showPage()
            add_logos()
            p.setFont("Helvetica-Bold", 16)
            p.drawCentredString(width / 2, height - 50, f"Designs for {category.name}")
            y_position = height - 120
            design_count = 0

        p.setFont("Helvetica-Bold", 12)
        text_width = p.stringWidth(design.title, "Helvetica-Bold", 12)
        x_position = (width - text_width) / 2
        p.drawString(x_position, y_position, design.title)

        p.setFont("Helvetica", 10)
        description = f"{design.description}"
        price = f"Price: {design.price}"
        
        desc_width = p.stringWidth(description, "Helvetica", 10)
        price_width = p.stringWidth(price, "Helvetica", 10)
        
        p.drawString((width - desc_width) / 2, y_position - 15, description)
        p.drawString((width - price_width) / 2, y_position - 30, price)

        y_image_position = y_position - 50
        images = design.images.all()

        if images:
            x_image_position = (width - (len(images) * 120)) / 2
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


@login_required(login_url='/vendor/login/')
def vendor_profile(request):
    vendor = Vendor.objects.get(user=request.user)
    # Organize orders by their status
    orders_by_status = {
        'placed': Order.objects.filter(vendor=vendor, order_status='Placed'),
        'in-making': Order.objects.filter(vendor=vendor, order_status='In Making'),
        'shipped': Order.objects.filter(vendor=vendor, order_status='Shipped'),
        'delivered': Order.objects.filter(vendor=vendor, order_status='Delivered'),
        'canceled': Order.objects.filter(vendor=vendor, order_status='Canceled'),
    }
    return render(request, 'vendor_profile.html', {'vendor': vendor, 'orders_by_status': orders_by_status})

@login_required(login_url='/vendor/login/')
def edit_vendor_profile(request):
    vendor = Vendor.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)  # Add request.FILES for file handling
        if form.is_valid():
            form.save()
            return redirect('vendor_profile')  # Redirect to the profile page after saving
    else:
        form = VendorProfileForm(instance=vendor)

    return render(request, 'edit_vendor_profile.html', {'form': form})

@csrf_exempt
def edit_vendor_logo(request):
    if request.method == 'POST':
        # Check if the file is received
        if 'shop_logo' in request.FILES:
            try:
                vendor = Vendor.objects.get(user=request.user)
                vendor.shop_logo = request.FILES['shop_logo']
                vendor.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No file found'})
    else:
        print("Request method is not POST.")
    return JsonResponse({'success': False})


# View to handle adding a new address
def add_address(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = AddressForm(data)
        if form.is_valid():
            # Save the new address, setting the vendor
            address = form.save(commit=False)
            address.vendor = request.user.vendor  # Assuming the user is a vendor
            address.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Form is not valid"})
    
def delete_address(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address_id = data.get('address_id')
            
            # Fetch and delete the address
            address = Address.objects.get(id=address_id)
            address.delete()
            
            return JsonResponse({'success': True})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def place_order(request):
    if request.method == 'POST':
        # Get the data from the POST request
        data = json.loads(request.body)
        design_id = data.get('design_id')
        quantity = data.get('quantity', 1)
        address_id = data.get('address_id')

        # Get the design and address
        try:
            design = Design.objects.get(id=design_id)
            address = Address.objects.get(id=address_id)
        except Design.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Design not found'})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Address not found'})

        # Ensure quantity is an integer and price is a Decimal
        try:
            quantity = int(quantity)  # Ensure quantity is an integer
            total_price = Decimal(design.price) * quantity  # Ensure price is a Decimal
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'Invalid quantity or price'})

        # Store the order temporarily and return success
        order = Order.objects.create(
            vendor=request.user.vendor,
            design=design,
            quantity=quantity,
            address=address,
            total_price=total_price
        )

        return JsonResponse({'success': True, 'message': 'Redirecting to payment.', 'order_id': order.id})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def fake_payment(request, order_id):
    # Get the order details
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('vendor_home')  # Redirect to vendor home if the order doesn't exist

    if request.method == 'POST':
        # Simulate payment success/failure
        payment_success = True  # Assume it's always successful for this fake payment

        if payment_success:
            # After successful payment, update the order status
            order.payment_status = 'Paid'
            order.order_status = 'Placed'
            order.save()

            messages.success(request, 'Payment successful! Your order is confirmed.')
            return redirect('payment_success')  # Redirect to payment success page

        else:
            messages.error(request, 'Payment failed! Please try again.')
            return redirect('payment_failure')  # Redirect to payment failure page

    return render(request, 'fake_payment_page.html', {'order': order})

def cancel_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            # Retrieve the order object
            order = Order.objects.get(id=order_id)

            # Cancel the order (you can add your own logic, e.g., marking it as 'Canceled')
            order.order_status = 'Canceled'
            order.save()

            messages.info(request, 'Your order has been canceled.')
            return redirect('vendor_home')  # Redirect to vendor home or a different page
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('vendor_home')  # Redirect to vendor home if order doesn't exist
    return redirect('vendor_home')

def payment_success(request):
    return render(request, 'payment_success.html')


def process_payment(request, order_id):
    try:
        # Get the order details by ID
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('vendor_home')  # Redirect to home if order doesn't exist

    if request.method == 'POST':
        # Simulate payment success/failure (this can be replaced with real payment logic)
        payment_success = True  # Set this to False for simulating failure

        if payment_success:
            # After successful payment, update the order status
            order.payment_status = 'Paid'
            order.save()

            messages.success(request, 'Payment successful! Your order is confirmed.')
            return redirect('payment_success')  # Redirect to payment success page
        else:
            order.payment_status = 'Failed'
            order.save()

            messages.error(request, 'Payment failed! Please try again.')
            return redirect('payment_failure')  # Redirect to failure page

    return redirect('vendor_home')  # Redirect to home if the method is not POST