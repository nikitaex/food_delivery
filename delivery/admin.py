from django.contrib import admin

from .models import Restaurant, Meal, CartMeal, Cart, Order, Customer, Complaint, User


admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(CartMeal)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Complaint)
