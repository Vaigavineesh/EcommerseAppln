from django.urls import path
from Customer import views

urlpatterns=[
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.loginview.as_view(),name="signin"),
    path("home/",views.IndexView.as_view(),name="home"),
    path("product/<int:id>",views.ProductDetailView.as_view(),name='product-detail'),
    path("products/<int:id>/carts/add",views.AddToCart.as_view(),name="cart-add"),
    path("customer/carts/all",views.CartListview.as_view(),name="carts-list"),
    path("carts/<int:id>/change",views.CartRemoveview.as_view(),name="cart-change"),
    path("orders/add/<int:id>",views.MakeOrderView.as_view(),name="make-order"),
    path("orders/all",views.Myorders.as_view(),name="myorders"),
    path("orders/<int:id>/change",views.OrderCancelView.as_view(),name="order-cancel"),
    path("offers/all",views.DiscountroductView.as_view(),name="offer-list"),
    path("review/<int:id>/add",views.ReviewCreateView.as_view(),name="review-add"),
    path("logout",views.signout_view,name="signout")
]