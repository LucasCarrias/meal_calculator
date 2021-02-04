from rest_framework import serializers
from .models import Meal
from dish.models import Dish
from chef.models import Chef
from category.models import Category


class MealWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class MealSerializer(serializers.ModelSerializer):
    dishes = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='dish-detail',
        queryset=Dish.objects.all()
    )
    chef = serializers.HyperlinkedRelatedField(
        view_name='chef-detail',
        queryset=Chef.objects.all()
    )
    categories = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='category-detail',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Meal
        fields = "__all__"


class MealCalculateSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_cost = serializers.FloatField()
    cooking_time = serializers.FloatField()
    total_portions = serializers.FloatField()