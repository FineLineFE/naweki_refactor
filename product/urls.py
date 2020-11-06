from django.urls import path
from .views      import ProductView,ProductListView 

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
]