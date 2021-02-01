from rest_framework import serializers
from .models import Chef


class SingUpSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):       
        return Chef.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ["username", "email", "rating"]
        read_only_fields = ['rating']