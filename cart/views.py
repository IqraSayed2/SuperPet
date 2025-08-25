from django.shortcuts import render, HttpResponseRedirect
from .models import Cart, CartItem, Order, OrderItem
from product.models import Product
from .forms import OrderForm
import uuid
import razorpay
from superpet.settings import RAZORPAY_ID,RAZORPAY_SECRET,EMAIL_HOST_USER
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import SignatureVerificationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def cart(request):
    current_user = request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    cartitems = cart.cartitem_set.all()
    total = 0
    for cartitem in cartitems:
        total+= cartitem.quantity*cartitem.products.product_price

    return render(request,"cart.html",{"cartitems":cartitems ,"total":total,"isEmpty":len(cartitems)==0})


@login_required(login_url='/login')
def add_to_cart(request,productId): 
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    CartItem.objects.get_or_create(cart=cart,products=Product.objects.get(id=productId))
    cartitem,cartitem_created=CartItem.objects.get_or_create(cart=cart,products=Product.objects.get(id=productId))
    quantity=int(request.GET.get('quantity'))

    if cartitem_created :
        cartitem.quantity = quantity
    else:
        cartitem.quantity = cartitem.quantity+quantity

    cartitem.save()

    print(request.META.get("HTTP_REFERER"))  #just to check in terminal (not important to write)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='/login')
def delete_cart_item(request,cartitem_id):
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='/login')
def update_cart_item(request,cartitem_id):
    cartitem = CartItem.objects.get(id=cartitem_id)
    quantity = request.GET.get("quantity")
    cartitem.quantity = quantity
    cartitem.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='/login')
def checkout(request):
    if request.method=="GET":
        form = OrderForm()
        return render(request,"checkout.html",{'form':form})
    elif request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            order = Order.objects.create(
                order_id = str(uuid.uuid4())[:11],
                user = request.user,
                address_line_1 = form.cleaned_data['address_line_1'],
                address_line_2 = form.cleaned_data['address_line_2'],
                city = form.cleaned_data['city'],
                state = form.cleaned_data['state'],
                pincode = form.cleaned_data['pincode'],
                phoneno = form.cleaned_data['phoneno'],
            )

        cart = Cart.objects.get(id=request.session.get('cart_id'))
        for cartitem in cart.cartitem_set.all():
            OrderItem.objects.create(
                order = order,
                products = cartitem.products,
                quantity = cartitem.quantity
            )
        return HttpResponseRedirect('/cart/payment/'+order.order_id)



@login_required(login_url='/login')
def payment(request,order_id):
    order = Order.objects.get(order_id=order_id)
    orderitems = order.orderitem_set.all()

    total = 0
    for orderitem in orderitems:
        total+=orderitem.quantity*orderitem.products.product_price

    client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))
    data = { "amount": total*100, "currency": "INR", "receipt": order_id }
    payment_details = client.order.create(data=data)
    print(payment_details)

    return render(request,"payment.html",{'total':total,'order':order,'razorpayid':RAZORPAY_ID,'payment':payment_details})
    

@login_required(login_url='/login')
@csrf_exempt
def payment_success(request, order_id):
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))

    try:
        payment_check=client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        if payment_check:
            order=Order.objects.get(order_id=order_id)
            order.paid=True
            order.save()

            cart = Cart.objects.get(id=request.session.get('cart_id'))
            for cartitem in cart.cartitem_set.all():
                cartitem.delete()

            email_body = render_to_string("email.html",{"orders":order.orderitem_set.all()})

            send_mail(
                "Order Placed Successfully",
                email_body,
                EMAIL_HOST_USER,
                ['priyanka.vibhute@itvedant.com','siyavisrani@gmail.com',request.user.email],
                fail_silently = False,           #agr true denge to exceptions nahi pata chalega
                html_message = email_body
            )


    except SignatureVerificationError:
        return render(request,'payment_failed.html')
    return render(request,'success.html')


@login_required(login_url='/login')
def orders(request):
    orders = Order.objects.filter(user = request.user)
    return render(request,'orders.html',{"orders":orders})

