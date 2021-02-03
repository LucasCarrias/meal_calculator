from rest_framework import serializers
from .models import Dish
from ingredient.models import Ingredient


class DishSerializer(serializers.ModelSerializer):
    ingredients = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='ingredient-detail',
        queryset=Ingredient.objects.all()
    )

    chef = serializers.HyperlinkedRelatedField(
        view_name='chef-detail',
        queryset=Ingredient.objects.all()
    )
    class Meta:
        model = Dish
        fields = "__all__"

class DishWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"