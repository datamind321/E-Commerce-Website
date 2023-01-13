from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render 
from account.models import Cart,CartIteams
from ecom.models import Product, SizeVariant 

# Create your views here.



def get_products(request,slug):
    # print('***')
    # print(request.user)
    # print('***')
    # print(request.user.profile.get_cart_count)

 
    try:
        product=Product.objects.get(slug=slug)
        context={'product':product}
        if request.GET.get('size'):
            size=request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size']=size
            context['updated_price']=price
            print(price)

        return render(request,'product/products.html',context=context)
    except Exception as e:
        print(e)








