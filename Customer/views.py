from django.shortcuts import render,redirect
from django.views.generic import View
from Customer.forms import Registration,loginform,ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from store.models import Products,Carts,Orders,Offers

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper
def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")
class SignUpView(View):
    def get(self,request,*args,**kw):
        form=Registration()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kw):
        form=Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
        else:
            return render(request,"signup.html",{"form":form})
class loginview(View):
    def get(self,request,*args,**kw):
        form=loginform()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kw):
        form=loginform(request.POST)
        if form.is_valid():
            usrname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(usrname,pwd)
            usr=authenticate(request,username=usrname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})  
@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kw):
        qs=Products.objects.all()
        return render(request,"index.html",{"products":qs})
@method_decorator(signin_required,name="dispatch")
class ProductDetailView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Products.objects.get(id=id)
        return render(request,"product-detail.html",{"product":qs})
@method_decorator(signin_required,name="dispatch")
class AddToCart(View):
    def post(self,request,*args,**kw):
        qty=request.POST.get("qty")
        user=request.user
        id=kw.get("id")
        product=Products.objects.get(id=id)
        Carts.objects.create(product=product,user=user,qty=qty)
        return redirect("home")
@method_decorator(signin_required,name="dispatch")
class CartListview(View):
    def get(self,request,*args,**kw):
        qs=Carts.objects.filter(user=request.user,status="in-cart")
        return render(request,"carts-list.html",{"carts":qs})
@method_decorator(signin_required,name="dispatch")
class CartRemoveview(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Carts.objects.filter(id=id).update(status="cancelled")
        return redirect("home")
@method_decorator(signin_required,name="dispatch")
class MakeOrderView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Carts.objects.get(id=id)
        return render(request,"checkout.html",{"cart":qs})
    def post(self,request,*args,**kw):
        user=request.user
        address=request.POST.get("address")
        id=kw.get("id")
        cart=Carts.objects.get(id=id)
        product=cart.product
        Orders.objects.create(product=product,user=user,address=address)
        cart.status="order-placed"
        cart.save()
        return redirect("home")
@method_decorator(signin_required,name="dispatch")
class Myorders(View):
    def get(self,request,*args,**kw):
        qs=Orders.objects.filter(user=request.user).exclude(status="cancelled")
        return render(request,"order-list.html",{"orders":qs})
@method_decorator(signin_required,name="dispatch")
class OrderCancelView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Orders.objects.filter(id=id).update(status="cancelled")
        return redirect("myorders")
@method_decorator(signin_required,name="dispatch")
class DiscountroductView(View):
    def get(self,request,*args,**kw):
        qs=Offers.objects.all()
        return render(request,"offer-products.html",{"offers":qs})
@method_decorator(signin_required,name="dispatch")
class ReviewCreateView(View):
    def get(self,request,*args,**kw):
        form=ReviewForm
        return render(request,"review-add.html",{"form":form})
    def post(self,request,*args,**kw):
        form=ReviewForm(request.POST)
        id=kw.get("id")
        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect("home")
        else:
            return render(request,"review-add.html",{"form":form})


