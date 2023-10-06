from django.contrib.auth import get_user_model
from rest_framework import serializers
from .utils import IntegerToDateField
from .models import Category, Brand, Shop, Product, ProductHistory, Request, Notifications

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    period_date = IntegerToDateField()

    class Meta:
        model = Request
        fields = (
            'user',
            'email_notification',
            'lk_notification',
            'notification_type',
            'endpoint',
            'price',
            'discount',
            'period_date',
        )


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = (
            'text',
            'created_at',
        )
