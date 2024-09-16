from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if(data['username']):
            if(User.objects.filter(username = data["username"])).exists():
                raise serializers.ValidationError('Username is taken')
        
        if(data['email']):
            if(User.objects.filter(email = data["email"])).exists():
                raise serializers.ValidationError('Username is taken')
        
        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

class RegisterRestaurantSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    restaurant_name = serializers.CharField()
    image_link = serializers.URLField()
    restaurant_rating = serializers.IntegerField()
    restaurant_area = serializers.CharField()

    def validate(self, data):
        if(data['username']):
            if(User.objects.filter(username = data["username"])).exists():
                raise serializers.ValidationError('Username is taken')
        
        if(data['email']):
            if(User.objects.filter(email = data["email"])).exists():
                raise serializers.ValidationError('Username is taken')
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.is_superuser = True
        user.save()

        restaurant = Restaurant.objects.create(restaurant_name=validated_data['restaurant_name'], restaurant_rating=validated_data['restaurant_rating'], restaurant_area=validated_data['restaurant_area'], image_link=validated_data['image_link'])


        RestaurantUserRelation.objects.create(
            user = user,
            restaurant = restaurant
        )

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        #exclude = ['name', 'age']
        fields = '__all__'
        # depth = 1

    
    def validate(self, data):
        if(data['age'] < 18):
            raise serializers.ValidationError('Age should be greater than 18')
        return data

class RestaurantSerializerForItem(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_id']

class ItemSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(source='restaurant.id', read_only=True)
    class Meta:
        model = RestaurantItems
        fields = ['id', 'restaurant_id', 'item_name', 'item_price', 'item_description']

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantItems
        fields = "__all__"
