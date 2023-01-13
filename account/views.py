from ecom.models import Coupan, Product, SizeVariant
from .models import Cart, CartIteams, Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def login_page(request):
    if request.method =="POST":

        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request,'account not found !') 
            return  HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_varified:
            messages.warning(request,'your account ia not varified !') 
            return  HttpResponseRedirect(request.path_info)

        user_obj=authenticate(username=email,password=password)
        if user_obj:
            login(request,user_obj)
            return render(request,'home/index.html')

        messages.warning(request,'Incorrect username or password') 
        return  HttpResponseRedirect(request.path_info)
    return render(request,'accounts/login.html')

def register_page(request):
    if request.method =="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request,'Email is already Exists!') 
            return  HttpResponseRedirect(request.path_info)
        user_obj=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request,'An Email has been sent on your mail.') 
        return  HttpResponseRedirect(request.path_info)






    return render(request,'accounts/register.html')


def activate_email(request,email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_varified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid Email token")


def add_to_cart(request,uid):
    variant=request.GET.get('variant')
    product=Product.objects.get(uid=uid)
    user=request.user
    cart , _ = Cart.objects.get_or_create(user=user,is_paid=False)
    cart_iteam=CartIteams.objects.create(cart=cart,product=product,)
    if variant:
        variant = request.GET.get('variant')
        size_variant=SizeVariant.objects.get(size_name=variant)
        cart_iteam.size_variant=size_variant
        cart_iteam.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request,cart_item_uid):
    try:
        cart_item=CartIteams.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


def cart(request):
    cart_obj=Cart.objects.get(is_paid=False,user=request.user)
    if request.method == "POST":
        coupan=request.POST.get('coupan')
        coupan_obj=Coupan.objects.filter(coupan_code__icontains = coupan)
        if not coupan_obj.exists():
            messages.warning(request,"Invalid Coupan !")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_obj.coupan:
            messages.warning(request,"Coupan Already Exist !")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() < coupan_obj[0].min_amount:
            messages.warning(request,f"Amount should be greater than Rs.{coupan_obj[0].min_amount}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupan_obj[0].is_expired:
            messages.warning(request,f"Coupan Expired !")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



        cart_obj.coupan=coupan_obj[0]
        cart_obj.save()
        messages.success(request,"Coupan Applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




        


    context= {'cart':cart_obj} 
    return render(request,'accounts/cart.html',context)



def remove_coupan(request,cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupan=None
    cart.save()
    messages.success(request,'Coupan Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





    

