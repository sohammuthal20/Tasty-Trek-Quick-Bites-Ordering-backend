from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adress = models.CharField(max_length=200)
    isRestaurant = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10)

class Restaurant(models.Model):
    image_link = models.CharField(max_length=10000)
    restaurant_name = models.CharField(max_length=100)
    restaurant_rating = models.FloatField()
    restaurant_area = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.restaurant_name

class RestaurantUserRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} : {self.restaurant.restaurant_name}"


class RestaurantTags(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    tags = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.tags}: {self.restaurant.restaurant_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000, default="Food Processing")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    def __str__(self) -> str:
        return self.user.username

class RestaurantItems(models.Model):
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_description = models.CharField(max_length=150)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return  f"{self.restaurant.restaurant_name}: {self.item_name}"

class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(RestaurantItems, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.orders.user.username}: {self.item.item_name}"