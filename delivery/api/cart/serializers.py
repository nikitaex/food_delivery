from rest_framework import serializers

from delivery.models import Cart, Customer, CartMeal, Order, Complaint
from delivery.api.main.serializers import MealSerializer


class CartMealSerializer(serializers.ModelSerializer):

    meal = MealSerializer()

    class Meta:
        model = CartMeal
        fields = ['id', 'meal', 'qty', 'final_price']


class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    @staticmethod
    def get_user(obj):
        if not (obj.user.first_name and obj.user.last_name):
            return obj.user.username
        return ' '.join([obj.user.first_name, obj.user.last_name])


class CartSerializer(serializers.ModelSerializer):

    meals = CartMealSerializer(many=True)
    owner = CustomerSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    cart_meal = CartMealSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'cart_meal', 'phone', 'address', 'status', 'created_at',
                  'delivered_at', 'courier']


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = '__all__'
