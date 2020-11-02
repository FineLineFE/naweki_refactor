import jwt
import json
from django.http              import JsonResponse
from naweki_refactor.settings import SECRET_KEY, ALGORITHM
from account.models           import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if "Authorization" not in request.headers:
            return JsonResponse({"message" : "NO_TOKEN_INVALID_USER"}, status = 401)

        try:
            access_token    = request.headers.get('Authorization')
            data            = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
            account         = Account.objects.get(id = data['id'])
            request.account = account.id
            
        except jwt.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
        
        except Account.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"} , status = 400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper