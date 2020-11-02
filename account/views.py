import re
import json
import bcrypt
import jwt
import requests
from django.views             import View
from django.http              import JsonResponse
from account.models           import Account
from naweki_refactor.settings import SECRET_KEY, ALGORITHM

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
                return JsonResponse({"message" : "WORNG_PASSWORD" } , status = 401)
            
            return JsonResponse({"message" : "WORNG_EMAIL"} , status = 401)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEYS"} , status = 400)         