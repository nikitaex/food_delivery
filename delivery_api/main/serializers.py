from rest_framework import serializers

from delivery.models import Meal, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['name', 'slug', 'address']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }


class MealSerializer(serializers.ModelSerializer):

    restaurant = RestaurantSerializer()

    class Meta:
        model = Meal
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }
