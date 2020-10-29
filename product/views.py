import json
from django.views import View
from django.http  import JsonResponse
from .models      import (Color, 
                          ProductColor, 
                          Product, 
                          Category, 
                          Type,
                          ProductSize,
                          Size,
                          SubImageUrl)  

class ProductListView(View):
    def get(self,request):
        product_list = [
            {
                "id"                 : product.id,
                "productImage"       : product.main_img_url,
                "name"               : product.name,
                "price"              : product.price,
                # "selectProductColor" : ,
            } for product in Product.objects.all()
        ]
        return JsonResponse({"message" : product_list}, status = 200)


# class ProdutView(View):
#     def get(self, request, product_id):
        
