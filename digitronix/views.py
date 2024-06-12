from django.shortcuts import redirect, render
from django.urls import reverse
from store_app.models import *
from django.db.models import Q
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def basic(request):
    return render(request, 'main/basic.html')

def account(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    orderItem = OrderItem.objects.filter(user=user)
    order = Order.objects.filter(user=user)
    orderaddress = Order.objects.filter(user=user).order_by('-date')[:2]
    # Separate code to combine address components and update the order list

    context = {
        'orderitem' : orderItem,
        'order': order,
        "orderaddress":orderaddress,
    }
    return render(request, 'main/account.html', context)

def yourorder(request):
    # wishlist = Product.objects.filter(wishlisted = True)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    order = OrderItem.objects.filter(user=user)
    print(order)
    context = {
        "order": order,
        # "wishlist": wishlist,
    }
    return render(request, 'main/yourorder.html', context)

def index(request):
    # wishlist = request.user.wishlist.all()
    product = Product.objects.filter(status = 'Publish')
    context = {
        "product": product,
        # "wishlist" : wishlist,
    }
    print(wishlist)
    return render(request, 'main/index.html', context)

def product(request):
    product = Product.objects.filter(status = 'Publish')
    # wishlist = Product.objects.filter(wishlisted = True)
    categories = Category.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    cat_id = request.GET.get('cat')
    fprice_id = request.GET.get('fprice')
    color_id = request.GET.get('colour')
    brand_id = request.GET.get('brand')
    name_AtoZ_id = request.GET.get('nAtoZ')
    name_ZtoA_id = request.GET.get('nZtoA')
    price_lotohi_id = request.GET.get('plotohi')
    price_phitolo_id = request.GET.get('phitolo')
    newprod_id = request.GET.get('newproduct')
    oldprod_id = request.GET.get('oldproduct')

# Filtering by specific models for specific requirement like filter by color, by filter_price, etc.
    if cat_id:
        product = Product.objects.filter(categories = cat_id, status = 'Publish')
    elif fprice_id:
        product = Product.objects.filter(filter_price = fprice_id, status = 'Publish')
    elif color_id:
        product = Product.objects.filter(color = color_id, status = 'Publish')
    elif brand_id:
        product = Product.objects.filter(brand = brand_id, status = 'Publish')

# Filtering by AtoZ and ZtoA names
    elif name_AtoZ_id:
        product = Product.objects.filter(status = 'Publish').order_by('name')
    elif name_ZtoA_id:
        product = Product.objects.filter(status = 'Publish').order_by('-name')

# Filtering by lowTohigh and highTolow prices
    elif price_lotohi_id:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif price_phitolo_id:
        product = Product.objects.filter(status = 'Publish').order_by('-price')

# Filtering by new and renewed(old) products
    elif newprod_id:
        product = Product.objects.filter(condition = 'New', status = 'Publish').order_by('-id')
    elif oldprod_id:
        product = Product.objects.filter(Q(condition = 'Renewed') | Q(condition = 'Renewed'), status = 'Publish').order_by('id')

# Returning all products in case of no filters applied.  
    else:
        product = Product.objects.filter(status = 'Publish')



    context = {
        'product': product,
        "categories": categories,
        "filter_price": filter_price,
        "color": color,
        "brand": brand,
        # "wishlist": wishlist
    }
    return render(request, 'main/product.html', context)


def search(request):
    search_text = request.GET.get('query', '')
    product = Product.objects.filter(name__icontains = search_text)
    context = {
        'product': product
    }
    return render(request, 'main/search.html', context)

def product_details(request, id):
    prod = Product.objects.filter(id=id).first()
    # wishlist = Product.objects.filter(wishlisted = True)
    context = {
        "prod": prod,
        # "wishlist": wishlist
    }
    return render(request, 'main/product_details.html', context)

def contactUs(request):
    # wishlist = Product.objects.filter(wishlisted = True)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = ContactUs(
            name = name,
            email = email,
            subject = subject,
            message = message
        )

        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        # recipient : A person who receives something.
        recipient_list = [settings.EMAIL_HOST_USER] # Using myemail as I dont to send email to users
        try:
            send_mail(subject, message, email_from, recipient_list)
            contact.save()
            return redirect('Index')
        except:
            return redirect('ContactUs')
    return render(request, 'main/contactus.html')

def handleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')
        
        customer = User.objects.create_user(username, email=email, password=pass1)
        customer.first_name = firstname
        customer.last_name = lastname
        customer.save()
        return redirect('HandleLogin')
    return render(request, "registration/auth.html")

@csrf_exempt
def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            return redirect('HandleLogin')
    return render(request, 'registration/auth.html')

def handleLogout(request):
    logout(request)
    return redirect('Index')


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("Index")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("CartDetail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("CartDetail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("CartDetail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("CartDetail")


@login_required(login_url="/login/")
def cart_detail(request):
    # wishlist = Product.objects.filter(wishlisted = True)
    return render(request, 'cart/cart_details.html')

@login_required(login_url="/login/")
def checkout(request):
    # wishlist = Product.objects.filter(wishlisted = True)
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        amount_float = float(amount_str)
        amount = float(amount_float)

    payment = client.order.create({
        "amount" : amount*100,
        "currency": "INR",
        "payment_capture": "1"
    })
    order_id = payment['id']

    context = {
        'payment': payment,
        'order_id': order_id,
        'amount': amount,
        # "wishlist": wishlist
    }
    return render(request, 'cart/checkout.html', context)

@login_required(login_url="/login/")
def placeorder(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        add_info = request.POST.get('message')

        order_id = request.POST.get('orderId')
        payment = request.POST.get('payment')
        # wishlist = Product.objects.filter(wishlisted = True)

        context = {
            'order_id' : order_id,
            # 'wishlist' : wishlist
        }
        order = Order(user = user,
                      firstname=firstname,
                      lastname=lastname,
                      country=country,
                      address=address,
                      city=city,
                      state=state,
                      postcode=postcode,
                      phone=phone,
                      email=email,
                      payment_id = order_id,
                      amount=amount,
                      additional_info = add_info)
        order.save()

        for i in cart:
            a = (float(cart[i]['price']))
            b = cart[i]['quantity']

            total = a * b
            
            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()

        return render(request, 'cart/placeorder.html', context)
    else:
        return redirect('PlaceOrder')

@csrf_exempt
def success(request):
    # wishlist = Product.objects.filter(wishlisted = True)
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key,value in a.items():
            if key == 'razorpay_order_id':
                order_id = value
                break
        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()
    # Clear the cart session data
    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'cart/thankyou.html')



# @login_required(login_url="/login/")
# def toggle_wishlist(request, product_id):
#     # product = get_object_or_404(Product, pk=product_id)
#     product = Product.objects.filter(pk=product_id).first()
#     product.wishlisted = not product.wishlisted
#     product.save()
#     # current_path = request.get_full_path()
#     previous_page = request.META.get('HTTP_REFERER', '/')
#     previous_page = request.META.get('HTTP_REFERER') or reverse('Index')
#     return redirect(previous_page, pk=product_id)

@login_required(login_url="/login/")
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.user in product.wishlisted_by.all():
        product.wishlisted_by.remove(request.user)  # Remove from wishlist
    else:
        product.wishlisted_by.add(request.user)  # Add to wishlist
    
    previous_page = request.META.get('HTTP_REFERER') or reverse('Index')
    return redirect(previous_page)

@login_required(login_url="/login/")
def wishlist(request):
    wishlist = request.user.wishlist.all()
    product = Product.objects.filter(status = 'Publish')
    context = {
        "product": product,
        "wishlist" : wishlist,
    }
    return render(request, 'main/wishlist.html', context)
