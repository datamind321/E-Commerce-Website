import uuid
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.emails import send_account_activation_email
from ecom.models import ColorVariant, Coupan, Product, SizeVariant



class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_varified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_image=models.ImageField(upload_to="profile")


    # def ready(self):
    #     from django.contrib.auth.models import User
    #     def get_cart_count(self):
    #         from account.models import CartIteams
    #         return CartIteams.object.filter(cart__is_paid=False,cart__user=self.user).count()
    #     User.add_to_class("get_cart_count",get_cart_count)

    def get_cart_count(self):
        return CartIteams.objects.filter(cart__is_paid= False ,cart__user=self.user).count()

      




class Cart(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    coupan=models.ForeignKey(Coupan , on_delete=models.SET_NULL,null=True,blank=True)
    is_paid=models.BooleanField(default=False)


    
    def get_cart_total(self):
        cart_itemo=self.cart_items.all()
        price = []
        for cart_iteam in cart_itemo:
            price.append(cart_iteam.product.price)
            
            if cart_iteam.color_variant:
                color_variant_price=cart_iteam.color_variant.price
                price.append(color_variant_price)

            if cart_iteam.size_variant:
                size_variant_price=cart_iteam.size_variant.price
                price.append(size_variant_price)
        
        if self.coupan:
           
            if self.coupan.min_amount < sum(price):
                return sum(price) - self.coupan.discount_price 
            
        print(sum(price))
        return sum(price)      



class CartIteams(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    color_variant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,null=True,blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) -> str:
            return self.product,self.size_variant




    def get_product_price(self):
        price=[self.product.price]

        if self.color_variant:
            color_variant_price=self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price=self.size_variant.price
            price.append(size_variant_price)
        return sum(price)





@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            
            email_token=str(uuid.uuid4()) 
            Profile.objects.create(user=instance,email_token=email_token)
            email=instance.email
            send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)










    
    
        

