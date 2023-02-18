from django.contrib import admin
from store.models import Category,Products,Offers
admin.site.register(Category)#u should enter this code after creating super user
admin.site.register(Products)
admin.site.register(Offers)
