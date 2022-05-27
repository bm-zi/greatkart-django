from django.shortcuts import get_object_or_404, render
from carts.models import Cart, CartItem
from .models import Product
from category.models import Category
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

from carts.views import _cart_id

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)     # show 1 products in page   
        page = request.GET.get('page')            
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else:        
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()
        paginator = Paginator(products, 3)        # show 3 products in page
        page = request.GET.get('page')            # get the variable page from the url
        paged_product = paginator.get_page(page)  # send this to template, instead of products

    context = {
        # 'products': products,
        'products': paged_product,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
        # For test purpose use the two following lines
        # return HttpResponse(in_cart)
        # exit()

    except Exception as e:
        raise e
        
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }    
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:   # if keyword has some value and not blank
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)