import json
from django.views             import View
from django.http              import JsonResponse
from account.models           import Account
from product.models           import Product, Size
from cart.models              import Cart
from naweki_refactor.settings import SECRET_KEY, ALGORITHM
from utils                    import login_decorator

class CartView(View):
    @login_decorator     
    def post(self, request):
        data = json.loads(request.body)  
        try:      
            if Cart.objects.filter(product_id = data['product_id'] , account_id = request.account).exists():
                return JsonResponse({"message" : "INVALID_REQUEST"}, status = 400)
              
            else:
                Cart.objects.create(
                    count      = data['count'],
                    account_id = request.account,
                    product_id = data['product_id'],               
                    size_id    = data['size_id'] 
                )
                return JsonResponse({"message" : "CREATE_SUCCESS"} , status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)   
        
    @login_decorator
    def get(self,request):
        cart_list = Cart.objects.filter(account_id = request.account).select_related('product', 'size')       
        cart_data = [{
            "cartId"       : data.id,
            "productId"    : data.product.id,
            "sizeId"       : data.size.id,
            "name"         : data.product.name,
            "price"        : int(data.product.price),
            "productImage" : data.product.main_img_url,
            "count"        : int(data.count)
            
        } for data in cart_list]
        return JsonResponse({"cart_list" : cart_data}, status = 200)
    
    @login_decorator
    def patch(self,request):
        data = json.loads(request.body)
        try:
            if not Cart.objects.filter(id = data['cart_id']).exists():
                return JsonResponse({"message" : "CART_NOT_EXISTS"}, status = 400)
            
            else :             
                cart_id          = data['cart_id']
                cart_count       = Cart.objects.get(id = cart_id)
                cart_count.count = int(data['count'])
                cart_count.save()
                return JsonResponse({"message" : "UPDATE_SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)
                          
    @login_decorator
    def delete(self,request):
        data = json.loads(request.body)
        try:
            if Cart.objects.filter(id = data['cart_id']).exists():
                Cart.objects.filter(id = data['cart_id']).delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"} , status = 200)
    
        except Cart.DoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST_CART"}, status = 404)