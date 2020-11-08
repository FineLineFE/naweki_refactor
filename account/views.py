import re
import json
import bcrypt
import jwt
import requests
from django.views             import View
from django.http              import JsonResponse
from .models                  import Account
from naweki_refactor.settings import SECRET_KEY, ALGORITHM
from utils                    import login_decorator

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "DUPLICATED_EMAIL"} , status = 400)

            if not re.match('^(?=^.{8,16}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$', data['password']):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400) 
            
            if re.match('^\d{3}-\d{4}-\d{4}$', data['phone_number']):
                return JsonResponse({"message" : "INVALUD_PHONE_NUMBER"}, status = 400)             
            
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            Account.objects.create(
                email        = data['email'], 
                password     = hashed_password.decode('utf-8'),
                name         = data['name'],
                phone_number = data['phone_number'],
            )
            return JsonResponse({"message" : "SIGNUP_SUCCESS"} , status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)
        
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email = data['email']).exists() :
                account = Account.objects.get(email = data['email'])
                
                if bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')) :
                    token = jwt.encode({'id' : account.id} , SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                    return JsonResponse({"Authorization" : token}, status = 200 )             
                return JsonResponse({"message" : "INVALID_INPUT" } , status = 401) 
        
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"} , status = 400)   
  
class WishListView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not WishList.objects.filter(product_id = data['product_id'], account_id = request.account).exists():
                return JsonResponse({"message" : "INVALID_REQUEST"}, status = 400)
            
            else:
                WishList.objects.create(
                    product_id = data['product_id'],
                    account_id = request.account_id
                )
                return JsonResponse({"message" : "ADD SUCCESS"}, status = 200)
            
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"}, status = 400)
    
    @login_decorator
    def get(self,request):
        wish = WishList.objects.filter(account_id = request.account).select_related('product', 'account')
        wish_data = [{
            "wishId"       : data.id,
            "accountId"    : data.account.id,
            "productId"    : data.product.id,
            "productName"  : data.product.name,
            "productPrice" : int(data.product.price)
        } for data in wish]
        
    @login_decorator
    def delete(self,request):
        data = json.loads(request.body)
        try:
            if WishList.objects.filter(id = data['wishlist_id']).exists():
                WishList.objects.filter(id = data['wishlist_id']).delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"}. status = 200)
            
        except Wishlist.DoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST_WISHLIST"}, stsua = 404)
