from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),

    path('auth-register', views.user_register),
    path('auth-login', views.user_login),
    path('auth-logout', views.user_logout),
    
    path('products', views.products),
    path('products/<int:id>', views.each_product),
    path('products/<int:id>/buy', views.buy_product),
    # path('buy-shiling'),

    # path('transactions'),
    # path('')
]