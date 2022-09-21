from urllib import request
from xml.dom.minidom import Identified
from django.shortcuts import render,redirect
from .models import Post,Product,Order
from django.views.generic import ListView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect

#Zarinpal

from django.shortcuts import redirect
import requests
import json

MERCHANT = '0275691a-add6-432f-b904-49257044b016'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 1100  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'https://nadiejafari.ir/verify/'




class StartingPageView(ListView):
    template_name="blog/starting_page.html"
    model=Post
    context_object_name="posts"

class AllPostView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    ordering=["-id"]
    context_object_name="all_posts"
    
class SinglePostView(View):
    template_name="blog/post-detail.html"
    model=Post
    context={}

    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id")
        }

        return render(request,"blog/post-detail.html",context)

    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post= Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment= comment_form.save(commit=False)
            comment.post=post
            comment_form.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))

        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)

def cartItems(cart):
    items=[]
    for item in cart:
        items.append(Product.objects.get(id=item))
    return items

def genItemsList(cart):
    cart_items = cartItems(cart)
    item_list = ""
    for item in cart_items:
        item_list += str(item.name)
        item_list += ","
    return item_list

def priceCart(cart):
    cart_items = cartItems(cart)
    price=0
    for item in cart_items:
       price += item.price
    '{0:g}'.format(price)
    if 0<price<=500000 :
        price=price+200000
    return ('%.15f' % price).rstrip('0').rstrip('.')

    

def books(request):
    if 'cart' not in request.session:
        request.session['cart']=[]
    cart= request.session['cart']
    request.session.set_expiry(0)
    store_items = Product.objects.all()
    ctx = {'store_items': store_items, 
    'cart_size':len(cart)}
    
    if request.method == "POST":
        cart.append(int(request.POST['obj_id']))
        return redirect('books')
    return render(request,"blog/books.html",ctx)

def cart(request):
    cart= request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart,'cart_size':len(cart),
    'cart_items':cartItems(cart),
    'total_price':priceCart(cart)}
    return render(request,"blog/cart.html",ctx)

def removefromcart(request):
    request.session.set_expiry(0)
    obj_to_remove = int(request.POST['obj_id'])
    obj_index = request.session['cart'].index(obj_to_remove)
    request.session['cart'].pop(obj_index)
    return redirect('cart')

def checkout(request):
    request.session.set_expiry(0)
    cart=request.session['cart']
    ctx = {'cart':cart,'cart_size':len(cart),'total_price':priceCart(cart)}
    return render(request,'blog/checkout.html',ctx)

def completeOrder(request):
    request.session.set_expiry(0)
    cart=request.session['cart']
    order = Order()
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.mobile = request.POST['mobile']
    order.postcode = request.POST['postcode']
    order.email = request.POST['email']
    order.items = genItemsList(cart)
    order.save()
    return render(request,'blog/complete_order.html', None)


def send_request(request):
    cart= request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart,'cart_size':len(cart),
    'cart_items':cartItems(cart),
    'total_price':priceCart(cart)}
    req_data = {
        "merchant_id": MERCHANT,
        "amount": priceCart(cart),
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('عملیات موفقیت آمیز بود. شماره پیگیری :  ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('عملیات به وسیله کاربر متوقف شد')



def about(request):
    return render(request,"blog/about-me.html")

def movies(request):
    return render(request,"blog/movies.html")

def contact(request):
    return render(request,"blog/contact-us.html")

