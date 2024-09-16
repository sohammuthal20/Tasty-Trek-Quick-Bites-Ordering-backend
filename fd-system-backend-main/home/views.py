from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from .models import Restaurant
from .serializers import *

@api_view(['GET', 'POST'])
def index(request):
    coursers = None
    if request.method == "POST":      
        data = request.data
        print(data)
        coursers = {
            'course_name': 'POST',
            'learn': ["flask", 'django'],
            'course_provider': 'Scaler'
        }
    else:
        coursers = {
            'course_name': 'GET',
            'learn': ["flask", 'django'],
            'course_provider': 'Scaler'
        }

    return Response(coursers)

def AdminLogin(request):
    if (request.method == 'POST'):
        username = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if not RestaurantUserRelation.objects.filter(user=user).exists():
            return render(request, 'home/login.html', {
                'error': True
            })

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('user'))
        else:
            return render(request, 'home/login.html', {
                'error': True
            })

    return render(request, 'home/login.html', {
        'error': False
    })

def AdminRegister(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        restaurant_name = request.POST["restaurant_name"]
        restaurant_area = request.POST["restaurant_area"]
        restaurant_rating = 4
        image_link = request.POST["image_link"]
        
        data = {
            "username": username,
            "password": password,
            "email": email,
            "restaurant_name": restaurant_name,
            "restaurant_area": restaurant_area,
            "image_link": image_link,
            "restaurant_rating": restaurant_rating
        }

        serializer = RegisterRestaurantSerializer(data = data)

        if not serializer.is_valid():
            return JsonResponse({'success': False, "messsage": serializer.errors})

        serializer.save()
        return redirect(reverse('login'))

    return render(request, 'home/register.html')

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def UserPage(request):
    if request.method == "POST":
        name = request.POST["name"]
        desription = request.POST["description"]
        price = request.POST["price"]
        user = request.user

        restaurant = RestaurantUserRelation.objects.get(user=user).restaurant

        RestaurantItems.objects.create(
            item_name = name,
            item_description = desription,
            item_price = price,
            restaurant = restaurant
        )

    return render(request, 'home/admin.html')

def ListItemPage(request):
    user = request.user
    restaurant = RestaurantUserRelation.objects.get(user=user).restaurant

    restaurant_items = RestaurantItems.objects.filter(restaurant=restaurant)

    return render(request, 'home/list_items.html', {
        "items": restaurant_items
    })
    

def OrdersPage(request):
    orders_list = []
    user = request.user

    restaurant = RestaurantUserRelation.objects.get(user=user).restaurant
    orders = Order.objects.filter(restaurant=restaurant)
    
    for order in orders:
        order_items = OrderItems.objects.filter(orders=order)
        print(order_items)
        order_price = 0
        order_obj = []
        done = {}

        for order_item in order_items:
            if(order_item.item.id in done):
                continue
            quant = 0
            done[order_item.item.id] = 1

            for od in order_items:
                if od.item.id == order_item.item.id:
                    quant += 1

            order_obj.append({
                "name": order_item.item.item_name, 
                "quantity": quant
                })
            order_price += order_item.item.item_price
        orders_list.append({"items": order_obj, "amount": order_price, "status": order.status, "id": order.id})
    
    print(orders_list)


    orders_string_array = []

    for order in orders_list:
        str_order = ""
        l = 0
        for item in order["items"]:
            # print(item["quantity"])
            str_order += item["name"] + " x " + str(item["quantity"]) + ", "
            l += 1
        print(order["status"])
        orders_string_array.append({
            "id": order["id"],
            "string": str_order,
            "amount": order["amount"],
            "status": order["status"],
            "items": l,
        })

    return render(request, 'home/orders.html', {
        "orders": orders_string_array,
    })

class OrderByRestaurant(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        orders_list = []

        data = request.data

        restaurant = Restaurant.objects.get(id=data["restaurant_id"])

        orders = Order.objects.filter(restaurant=restaurant)
        
        for order in orders:
            order_items = OrderItems.objects.filter(orders=order)
            print(order_items)
            order_price = 0
            order_obj = []
            done = {}

            for order_item in order_items:
                if(order_item.item.id in done):
                    continue
                quant = 0
                done[order_item.item.id] = 1

                for od in order_items:
                    if od.item.id == order_item.item.id:
                        quant += 1

                order_obj.append({
                    "name": order_item.item.item_name, 
                    "quantity": quant
                    })
                order_price += order_item.item.item_price
            orders_list.append({"items": order_obj, "amount": order_price, "status": order.status})
        
        print(orders_list)


        orders_string_array = []
    
        for order in orders_list:
            str_order = ""
            for item in order["items"]:
                # print(item["quantity"])
                str_order += item["name"] + " x " + str(item["quantity"]) + " "
            orders_string_array.append({
                "string": str_order,
                "amount": order["amount"],
                "status": order["status"]
            })
        
        print(orders_string_array)

        return Response(orders_list)


class OrderByUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        orders_list = []
        user = request.user

        orders = Order.objects.filter(user=user)
        
        for order in orders:
            order_items = OrderItems.objects.filter(orders=order)
            print(order_items)
            order_price = 0
            order_obj = []
            done = {}

            for order_item in order_items:
                if(order_item.item.id in done):
                    continue
                quant = 0
                done[order_item.item.id] = 1

                for od in order_items:
                    if od.item.id == order_item.item.id:
                        quant += 1

                order_obj.append({
                    "name": order_item.item.item_name, 
                    "quantity": quant
                    })
                order_price += order_item.item.item_price
            orders_list.append({"items": order_obj, "amount": order_price, "status": order.status})
        
        print(orders_list)
        return Response(orders_list)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        restaurant_order = request.data
        restaurant = Restaurant.objects.get(id=request.data["restaurant"])
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant
        )

        print(restaurant_order["order"])

        for item, quant in restaurant_order["order"].items():
            print(item, quant)
            res_item = RestaurantItems.objects.get(id=int(item))
            quant2 = quant

            while(quant2>0):
                order_items = OrderItems.objects.create(
                    user=request.user,
                    orders=order,
                    item=res_item
                )
                quant2 -= 1
    
        return JsonResponse({
            "success": True, 
            "message": "Order has been created!"
        })


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        
        if not serializer.is_valid():
            return Response({"mesdsage": serializer.errors}, 400)

        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({"message": "Invalid Credentials"})

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"success": True, "message": "Logged In", "token": str(token)}, 201)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({'success': False, "messsage": serializer.errors}, 400)

        serializer.save()

        return Response({'success': True, 'message': "user created"}, 201)

class CreateItemAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateItemSerializer(data = data)

        if not serializer.is_valid():
            return Response({'success': False, "messsage": serializer.errors}, 400)

        serializer.save()

        return Response({'success': True, 'message': "item created"}, 201)


class RegisterRestaurantAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterRestaurantSerializer(data = data)

        if not serializer.is_valid():
            return Response({'success': False, "messsage": serializer.errors}, 400)

        serializer.save()
        return Response({'success': True, 'message': "user and restaurant created"}, 201)


class ItemView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    def get(self, request):
        objs = RestaurantItems.objects.all()
        serializer = ItemSerializer(objs, many=True)

        return Response({"items": serializer.data})

class ItemByRestaurantIDView(APIView):
    def get(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        objs = RestaurantItems.objects.filter(restaurant=restaurant)
        serializer = ItemSerializer(objs, many=True)

        return Response({"items": serializer.data})

class RestaurantView(APIView):
    def get(self, request):
        objs = Restaurant.objects.all()
        serializer = RestaurantSerializer(objs, many=True)

        return Response({"restaurants": serializer.data})

class ChangeOrderStatus(APIView):
    def post(self, request):
        data = request.data
        id = int(data["id"])

        order = Order.objects.get(id=id)
        order.status = data["status"]
        order.save()

        return Response({
            "message": "Done!"
        })

    # def post(self, request):
    #     data = request.data
    #     serializer = RestaurantSerializer(data = data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.validated_data)
    #     return Response(serializer.errors)
