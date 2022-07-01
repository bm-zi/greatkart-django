from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
    # if we need to show the products based on created_date, ascendently we use following
    # products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    products = Product.objects.all().filter(is_available=True).order_by('created_date')


    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)

