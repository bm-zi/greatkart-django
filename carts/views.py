from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
# from django.http import HttpResponse

# Create your views here.

def _cart_id(request):
    '''Returns the session id inside of cookies
    This is a private function.
    '''
    cart = request.session.session_key  
    # cart takes the session id inside of the cookies, extracted 
    # from argument request.  
    
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    ''' Adds the product to the card.
    This function used when clicked on 'Add to cart' button for a product
    '''
    product = Product.objects.get(id=product_id)  # get the product
    try:
        # Get the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()


    # Combine the cart and product to get the cart_item.
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # The value of column 'quantity' for object cart_item  has to be 
        # incremented as we click on 'Add to cart
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart, 
        )
        cart_item.save()

    # this following two lines added just for test, will be removed later.
    # return HttpResponse(cart_item.quantity) 
    # exit()

    # Or check the redirection to cart page by product name, like:
    # return HttpResponse(cart_item.quantity)
    # exit()

    # When the adding to cart operations is done, redirect user to cart.html page.
    return redirect('cart')


def remove_cart(request, product_id):
    '''Decrements the cart item'''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        # Tax added is 2%
        tax = (2 * total)/100
        grand_total = total + tax


    except cart.DoesNotExist:
        pass # just ignore

    context ={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
