from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser, Products, Transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
def home(request):
    data = {
        'title': 'Shiling Market Api Version 0.1',
        'message': 'Welcome To Our Api.',
    }
    return JsonResponse(data, safe=False)

def user_register(request):
    if request.method == 'POST':
        register_data = json.loads(request.body)
        try:
            first_name = register_data['first_name']
            last_name = register_data['last_name']
            username = register_data['username']
            email = register_data['email']
            password = register_data['password']
            password_confirm = register_data['password_confirm']
        except Exception as e:
            data = {
        'message': f'{e}',
    }
            return JsonResponse(data, safe=False, status = 403)
        if (first_name == "" or
            last_name == "" or
            username == "" or
            email == "" or
            password == "" or
            password_confirm == ""):
            data = {
        'message': 'All Fields Have To Be Filled',
    }
            return JsonResponse(data, safe=False, status = 403)
        elif (password != password_confirm):
            data = {
        'message': 'Passwords Didn\'t Match',
    }
            return JsonResponse(data, safe=False, status = 403)
        else:
            try:
                commit = CustomUser(first_name = first_name, 
                              last_name = last_name, 
                              username = username, 
                              email = email, 
                              password = make_password(password))
                commit.save()
            except Exception as e:
                data = {
        'message': str(e),
    }
                return JsonResponse(data, safe=False, status = 403)
            data = {
        'message': 'User Registerd Successfully.',
    }
            return JsonResponse(data, safe=False)
    else:
        data = {
        'message': f'{request.method} method is not allowed here POST only.',
    }
        return JsonResponse(data, safe=False, status = 405)
        
def user_login(request):
    if request.method == 'POST':
        # username = request.POST['username']
        login_data = json.loads(request.body)
        username = login_data['username']
        password = login_data['password']

        user = authenticate(username = username,password = password)

        if user is not None:
            login(request, user)
            data = {
        'message': f'User {user.get_username()} Logged in Successfully.',
    }
            return JsonResponse(data, safe=False)
        else:
            data = {
        'message': 'Invalid Credintials.',
    }
            return JsonResponse(data, safe=False, status = 400)
    else:
        data = {
        'message': f'{request.method} method is not allowed here POST only.',
    }
        return JsonResponse(data, safe=False, status = 405)
    
def user_logout(request):
    if request.user.is_authenticated:
        data = {
            'message': f'User {request.user.username} Logged out Sucessfully',
        }
        logout(request)
        return JsonResponse(data, safe=False, status = 200)
    else:
        data = {
            'message': f'No User Logged In.',
        }
        return JsonResponse(data, safe=False, status = 400)
    
def products(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                product_data = json.loads(request.body)
                name = product_data['name']
                description = product_data['description']
                images = product_data['images']
                price = product_data['price']
                quantity = product_data['quantity']
                user = request.user
            except Exception as e:
                data = {
                    "message": f'{e}'
                }
                return JsonResponse(data, safe=False, status = 403)
            if (name != "" or
                description != "" or
                price != ""):
                commit = Products(name = name, 
                            description = description, 
                            quantity = quantity,
                            image = images, 
                            price = price, 
                            user = user)
                commit.save()
                data = {
                    'messsage':'Product Registerd Sucessfully'
                }
                return JsonResponse(data, safe=False, status = 200)
            else:
                data = {
                    'messsage':'All Required Fields Must Be Filled'
                }
                return JsonResponse(data, safe=False, status = 403)
        else:
            data = {
                    'messsage':'Login First To Add A Product'
                }
            return JsonResponse(data, safe=False, status = 403)
    elif request.method == 'GET':
        products = Products.objects.values()
        
        return JsonResponse(list(products), safe=False, status = 200)
    
def each_product(request, id):
    products = Products.objects.filter(id = id).values()

    return JsonResponse(list(products), safe=False)

def buy_product(request, id):
    if request.method == 'POST':
        buy_data = json.loads(request.body)
        quantity = buy_data['quantity']
        
        try:
            buyer = CustomUser.objects.get(id = request.user.id)
            product = Products.objects.get(id = id)
        except Exception as e:
            data = {
                    'message': f'{e}'
                }
            return JsonResponse(data, safe=False, status = 403)
        seller = CustomUser.objects.get(id = product.user_id)

        if buyer.username == seller.username:
            data = {
                'message': f'A user can\'t buy from itself'    
            }
            return JsonResponse(data, safe=False, status = 403)
        else:
            data = {
            'buyer': f'{buyer.username}',
            'product': f'{product.name}',
            'seller': f'{seller.username}',
            'amount': f'{product.price}'
        }
            if (buyer.balance >= float(product.price)):
                if (int(quantity) <= product.quantity):
                    buyer.balance -= product.price
                    seller.balance += product.price
                    product.quantity -= int(quantity)
                    buyer.save(force_update=True)
                    seller.save(force_update=True)
                    product.save(force_update=True)

                    commit = Transaction(seller = seller, 
                                         buyer = buyer, 
                                         product = product)
                    commit.save()

                    if (product.quantity == 0):
                        product.delete()

                    data = {
                        'message': f'Product: {product.name} Bought Successfully by User: {buyer.username} from User: {product.user}'
                    }
                    return JsonResponse(data, safe=False, status = 200)
                else:
                    data = {
                        'message': f'Not Enough Product In Store'
                    }
                    return JsonResponse(data, safe=False, status = 404)

# def buy_shiling(request):
#     if request.user.is_authenticated:
