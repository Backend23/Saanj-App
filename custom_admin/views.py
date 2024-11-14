from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.shortcuts import render, get_object_or_404
from django.views import View


# Category Views

# Fetch all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'custom_admin/cat.html', {'categories': categories})

# Fetch all categories as JSON (used by JavaScript to dynamically update the page)
def get_categories_json(request):
    categories = Category.objects.values('id', 'name', 'description', 'status')
    return JsonResponse(list(categories), safe=False)

def get_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'status': category.status
        })
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found'}, status=404)

# Add or edit category
@csrf_exempt
def add_or_edit_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        name = request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        status = request.POST.get('categoryStatus')
        
        if category_id:
            # Edit existing category
            category = Category.objects.get(id=category_id)
            category.name = name
            category.description = description
            category.status = status
            category.save()
            return JsonResponse({'message': 'Category updated successfully', 'status': 'success'})
        else:
            # Add new category
            category = Category(name=name, description=description, status=status)
            category.save()
            return JsonResponse({'message': 'Category added successfully', 'status': 'success'})
    return JsonResponse({'message': 'Invalid request', 'status': 'error'})

# Delete category
@csrf_exempt
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({'message': 'Category deleted successfully', 'status': 'success'})
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found', 'status': 'error'})

# Toggle category status
@csrf_exempt
def toggle_category_status(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.status = 'inactive' if category.status == 'active' else 'active'
        category.save()
        return JsonResponse({'message': f'Category {category.status} successfully', 'status': 'success'})
    except Category.DoesNotExist:
        return JsonResponse({'message': 'Category not found', 'status': 'error'})

# Subcategory Views
# Fetch all subcategories as JSON
def get_subcategories_json(request):
    subcategories = Subcategory.objects.values('id', 'name', 'description', 'status', 'category_id')
    return JsonResponse(list(subcategories), safe=False)


def get_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    return JsonResponse({
        'id': subcategory.id,
        'name': subcategory.name,
        'description': subcategory.description,
        'status': subcategory.status,
        'categoryId': subcategory.category.id
    })

# Add or edit subcategory
@csrf_exempt
def add_or_edit_subcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('id')
        category_id = request.POST.get('parentCategory')
        name = request.POST.get('subcategoryName')
        description = request.POST.get('subcategoryDescription')
        status = request.POST.get('subcategoryStatus')

        category = get_object_or_404(Category, id=category_id)
        
        if subcategory_id:
            # Edit existing subcategory
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            subcategory.name = name
            subcategory.description = description
            subcategory.status = status
            subcategory.category = category
            subcategory.save()
            return JsonResponse({'message': 'Subcategory updated successfully', 'status': 'success'})
        else:
            # Add new subcategory
            subcategory = Subcategory(name=name, description=description, status=status, category=category)
            subcategory.save()
            return JsonResponse({'message': 'Subcategory added successfully', 'status': 'success'})
    
    return JsonResponse({'message': 'Invalid request', 'status': 'error'})

# Delete subcategory
@csrf_exempt
def delete_subcategory(request, subcategory_id):
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        subcategory.delete()
        return JsonResponse({'message': 'Subcategory deleted successfully', 'status': 'success'})
    except Subcategory.DoesNotExist:
        return JsonResponse({'message': 'Subcategory not found', 'status': 'error'})

# Toggle subcategory status
@csrf_exempt
def toggle_subcategory_status(request, subcategory_id):
    try:
        subcategory = Subcategory.objects.get(id=subcategory_id)
        subcategory.status = 'inactive' if subcategory.status == 'active' else 'active'
        subcategory.save()
        return JsonResponse({'message': f'Subcategory {subcategory.status} successfully', 'status': 'success'})
    except Subcategory.DoesNotExist:
        return JsonResponse({'message': 'Subcategory not found', 'status': 'error'})
    


# Metal Type Views
@csrf_exempt
def get_metal_types_json(request):
    """
    Fetches all metal types in JSON format for frontend rendering.
    """
    metal_types = MetalType.objects.values('id', 'name', 'purity', 'code', 'status')
    return JsonResponse(list(metal_types), safe = False)


@csrf_exempt
def get_metal_type(request, id):
    """
    Fetches a specific metal type by ID.
    """
    metal_type = get_object_or_404(MetalType, id=id)  # Use get_object_or_404 for consistency
    return JsonResponse({
        'id': metal_type.id,
        'name': metal_type.name,
        'purity': metal_type.purity,
        'code': metal_type.code,
        'status': metal_type.status
    })
    

@csrf_exempt
def add_or_edit_metal_type(request):
    """
    Adds or edits a metal type based on the provided data.
    - If an ID is provided in the data, it will edit the existing metal type.
    - Otherwise, it will create a new metal type.
    """
    if request.method == 'POST':
        # Access the form data directly from request.POST
        metal_id = request.POST.get('id')
        name = request.POST.get('metalName')
        purity = request.POST.get('metalPurity')
        code = request.POST.get('metalCode')
        status = request.POST.get('metalStatus')

        # Check for code uniqueness
        if MetalType.objects.filter(code=code).exclude(id=metal_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Metal code must be unique'})

        if metal_id:
            # Edit existing metal type
            try:
                metal_type = MetalType.objects.get(id=metal_id)
                metal_type.name = name
                metal_type.purity = purity
                metal_type.code = code
                metal_type.status = status
                metal_type.save()
                return JsonResponse({'status': 'success', 'message': 'Metal type updated successfully'})
            except MetalType.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Metal type not found'})
        else:
            # Add new metal type
            MetalType.objects.create(
                name=name,
                purity=purity,
                code=code,
                status=status
            )
            return JsonResponse({'status': 'success', 'message': 'Metal type added successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def delete_metal_type(request, id):
    """
    Deletes a metal type by ID.
    """
    try:
        MetalType.objects.get(id=id).delete()
        return JsonResponse({'status': 'success', 'message': 'Metal type deleted successfully'})
    except MetalType.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Metal type not found'})

@csrf_exempt
def toggle_metal_status(request, id):
    """
    Toggles the status of a metal type between 'active' and 'inactive'.
    """
    try:
        metal_type = MetalType.objects.get(id=id)
        metal_type.status = 'inactive' if metal_type.status == 'active' else 'active'
        metal_type.save()
        return JsonResponse({'status': 'success', 'message': f'Metal type status updated to {metal_type.status}'})
    except MetalType.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Metal type not found'})

# Weight Option Views
@csrf_exempt
def get_weight_options_json(request):
    """
    Fetches all weight options in JSON format for frontend rendering.
    """
    weight_options = WeightOption.objects.values('id', 'name', 'min_weight', 'max_weight', 'status')
    return JsonResponse(list(weight_options), safe = False)
                        

@csrf_exempt
def get_weight_option(request, id):
    """
    Fetches a specific weight option by ID.
    """
    weight_option = get_object_or_404(WeightOption, id=id)  # Use get_object_or_404 for consistency
    return JsonResponse({
        'id': weight_option.id,
        'name': weight_option.name,
        'min_weight': str(weight_option.min_weight),  # Ensure min_weight is returned as string for consistency
        'max_weight': str(weight_option.max_weight),  # Same for max_weight
        'status': weight_option.status
    })

@csrf_exempt
def add_or_edit_weight_option(request):
    """
    Adds or edits a weight option based on the provided data.
    - If an ID is provided in the data, it will edit the existing weight option.
    - Otherwise, it will create a new weight option.
    """
    if request.method == 'POST':
        # Get form data from the request body
        name = request.POST.get('name')
        min_weight = request.POST.get('minWeight')
        max_weight = request.POST.get('maxWeight')
        status = request.POST.get('status')
        weight_option_id = request.POST.get('id')

        # Check if the min_weight and max_weight are provided and valid
        try:
            min_weight = float(min_weight)
            max_weight = float(max_weight)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid weight values'}, status=400)

        if min_weight > max_weight:
            return JsonResponse({'status': 'error', 'message': 'Min weight cannot be greater than max weight'}, status=400)

        # Edit or create weight option
        if weight_option_id:
            # Edit existing weight option
            try:
                weight_option = WeightOption.objects.get(id=weight_option_id)
                weight_option.name = name
                weight_option.min_weight = min_weight
                weight_option.max_weight = max_weight
                weight_option.status = status
                weight_option.save()
                return JsonResponse({'status': 'success', 'message': 'Weight option updated successfully'})
            except WeightOption.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Weight option not found'}, status=404)
        else:
            # Add new weight option
            weight_option = WeightOption.objects.create(
                name=name,
                min_weight=min_weight,
                max_weight=max_weight,
                status=status
            )
            return JsonResponse({'status': 'success', 'message': 'Weight option added successfully'})

@csrf_exempt
def delete_weight_option(request, id):
    """
    Deletes a weight option by ID.
    """
    try:
        WeightOption.objects.get(id=id).delete()
        return JsonResponse({'status': 'success', 'message': 'Weight option deleted successfully'})
    except WeightOption.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Weight option not found'})

@csrf_exempt
def toggle_weight_status(request, id):
    """
    Toggles the status of a weight option between 'active' and 'inactive'.
    """
    try:
        weight_option = WeightOption.objects.get(id=id)
        weight_option.status = 'inactive' if weight_option.status == 'active' else 'active'
        weight_option.save()
        return JsonResponse({'status': 'success', 'message': f'Weight option status updated to {weight_option.status}'})
    except WeightOption.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Weight option not found'})
    

# Fetch all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'custom_admin/product.html', {'products': products})

# Fetch all products as JSON (used by JavaScript to dynamically update the page)
def get_products_json(request):
    products = Product.objects.values('id', 'title', 'description', 'weight', 'status', 'image_url', 'video_url')
    return JsonResponse(list(products), safe=False)

# Fetch a single product by ID
def get_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'weight': product.weight,
            'status': product.status,
            'image_url': product.image_url,
            'video_url': product.video_url,
            'categories': list(product.categories.values('id', 'name')),
            'subcategories': list(product.subcategories.values('id', 'name')),
            'metal_type': product.metal_type,
        })
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)

# Add or edit product
@csrf_exempt
def add_or_edit_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        title = request.POST.get('productTitle')
        description = request.POST.get('productDescription')
        weight = request.POST.get('productWeight')
        status = request.POST.get('productStatus')
        categories = request.POST.getlist('categories')
        subcategories = request.POST.getlist('subcategories')
        metal_type_id = request.POST.get('metalType')
        image_url = request.POST.get('image')  # Handle image URL
        video_url = request.POST.get('video')  # Handle video URL

        if product_id:
            # Edit existing product
            product = Product.objects.get(id=product_id)
            product.title = title
            product.description = description
            product.weight = weight
            product.status = status
            product.image_url = image_url
            product.video_url = video_url
            product.metal_type_id = metal_type_id
            product.categories.set(categories)
            product.subcategories.set(subcategories)
            product.save()
            return JsonResponse({'message': 'Product updated successfully', 'status': 'success'})
        else:
            # Add new product
            product = Product(
                title=title,
                description=description,
                weight=weight,
                status=status,
                image_url=image_url,
                video_url=video_url,
                metal_type_id=metal_type_id
            )
            product.save()
            product.categories.set(categories)
            product.subcategories.set(subcategories)
            return JsonResponse({'message': 'Product added successfully', 'status': 'success'})
    return JsonResponse({'message': 'Invalid request', 'status': 'error'})

# Delete product
@csrf_exempt
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully', 'status': 'success'})
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found', 'status': 'error'})

# Toggle product status
@csrf_exempt
def toggle_product_status(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.status = 'inactive' if product.status == 'active' else 'active'
        product.save()
        return JsonResponse({'message': f'Product {product.status} successfully', 'status': 'success'})
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found', 'status': 'error'})