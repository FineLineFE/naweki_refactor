from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('product', include('product.urls')),
    path('cart', include('cart.urls')),
]