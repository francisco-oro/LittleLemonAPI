from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers
from LittleLemonAPI.models import Category, Cart, OrderItem, MenuItem, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        write_only=True
    )

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('unit_price', 'price', 'menu_item')

    def create(self, validated_data):
        menu_item = validated_data.pop('menu_item_id')
        quantity = validated_data.pop('quantity')
        unit_price = menu_item.price
        price = unit_price * quantity

        cart = Cart.objects.create(
            menu_item=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            price=price,
            **validated_data
        )

        return cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

    def create(self, validated_data):
        validated_data["slug"] = slugify(validated_data["title"])
        category, _ = Category.objects.get_or_create(**validated_data)
        return category


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'delivery_crew', 'status', 'total', 'date', 'orderitem_set']
        read_only_fields = ('total', 'date')
