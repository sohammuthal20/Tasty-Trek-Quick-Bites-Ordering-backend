from django.contrib import admin
from .models import Restaurant
from .models import UserInfo
from .models import RestaurantTags
from .models import Order
from .models import RestaurantItems
from .models import OrderItems
from .models import RestaurantUserRelation



# Register your models here.
admin.site.register(Restaurant)
admin.site.register(UserInfo)
admin.site.register(RestaurantTags)
admin.site.register(Order)
admin.site.register(RestaurantItems)
admin.site.register(OrderItems)
admin.site.register(RestaurantUserRelation)