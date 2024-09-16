from home import views
from django.urls import path

urlpatterns = [
    path('restaurants/all/', views.RestaurantView.as_view()),
    path('items/all/', views.ItemView.as_view()),
    path('items/<int:id>/', views.ItemByRestaurantIDView.as_view()),
    path('register-restaurant/', views.RegisterRestaurantAPI.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('order/', views.OrderView.as_view()),
    path('myorders/', views.OrderByUserView.as_view()),
    path('create-item/', views.CreateItemAPI.as_view()),
    path('restaurant-orders/', views.OrderByRestaurant.as_view()),
    path('change-status/', views.ChangeOrderStatus.as_view()),
]
