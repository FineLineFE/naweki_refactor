import json
import jwt
import bcrypt

from django.test              import TestCase, Client

from naweki_refactor.settings import SECRET_KEY, ALGORITHM
from .models                  import Account

client = Client()

class SignUpTest(TestCase):
    
    def setUp(self):
        Account.objects.create(
            email        = 'user1@naver.com',
            password     = '1q2w3e4r5t@',
            name         = 'user1',
            phone_number = '01077778888'
        )
        
    def tearDown(self):
        Account.objects.all().delete()   
      
    def test_signup_success(self):
        account = {
            'email'        : 'user2@naver.com',
            'password'     : '5t4r3e2w1q@',
            'name'         : 'user2',
            'phone_number' : '01088888888'
        }
        response = client.post('/account/signup', json.dumps(account), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SIGNUP_SUCCESS'})
      
    def test_signup_fail_invalid_phone_number(self):
        account = {
            'email'        : 'usssser1@naver.com',
            'password'     : '1q2w3e4r5t@@',
            'name'         : 'user1',
            'phone_number' : '010-8888-8888'            
        }
        response = client.post('/account/signup', json.dumps(account), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PHONE_NUMBER'})
        
    def test_signup_fail_duplicated_email(self):
        account = {
            'email'        : 'user1@naver.com',
            'password'     : '1q2w3e4r5t@',
            'name'         : 'user1',
            'phone_number' : '01077778888'
        }
        response = client.post('/account/signup', json.dumps(account), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'DUPLICATED_EMAIL'})

    def test_signup_fail_invalid_password(self):
        data = {
            'email'        : 'user1111@naver.com',
            'password'     : '123456789',
            'name'         : 'user1',
            'phone_number' : '01077778888'
        }
        response = client.post('/account/signup', json.dumps(data), content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})