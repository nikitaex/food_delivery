from django.contrib import admin

from .models import Restaurant, Meal, CartMeal, Cart, Order, Customer, Restaurateur, Courier, Complaint


admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(CartMeal)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Restaurateur)
admin.site.register(Courier)
admin.site.register(Complaint)
