import json
from django.views import View
from django.http  import JsonResponse
from .models      import Color, ProductColor, Product, Category, Type, ProductSize, Size, SubImageUrl

class ProductListView(View):
    def get(self,request):
        product_list = [
            {
                "id"                 : product.id,
                "productImage"       : product.main_img_url,
                "name"               : product.name,
                "price"              : int(product.price),
            } for product in Product.objects.all()
        ]
        return JsonResponse({"message" : product_list}, status = 200)

class ProductView(View):
    def get(self, request, product_id):
        try:            
            selected_product = Product.objects.select_related('category','type').prefetch_related('subimageurl_set').get(pk = product_id)             
            selected_colors  = ProductColor.objects.select_related('color','product').filter(pk = product_id).all()
            selected_sizes   = ProductSize.objects.select_related('size', 'product').filter(pk = product_id).all()

            data = { 
                "categoryId" : selected_product.category.id,
                "colorId"    : selected_colors[0].color.id,
                "colorName"  : selected_colors[0].color.name,
                "content"    : selected_product.description_content,
                "id"         : selected_product.id,
                "imageUrl"   : [image.image_url for image in selected_product.subimageurl_set.all()],
                "name"       : selected_product.name,
                "price"      : int(selected_product.price),
                "sizeId"     : selected_sizes[0].size.id,
                "sizeName"   : selected_sizes[0].size.name,
                "title"      : selected_product.description_title,
                "color"      : [color.color_id for color in selected_product.productcolor_set.all()],
                "size"       : [size.size_id for size in selected_product.productsize_set.all()], 
                "typeId"     : selected_product.type.id
            }
            return JsonResponse({"message" : data}, status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status = 400)