import jwt
import bcrypt
import json
import datetime
from django.test              import TestCase, Client
from naweki_refactor.settings import SECRET_KEY, ALGORITHM
from utils                    import login_decorator
from account.models           import Account
from product.models           import Product, Size, Category, Size, Type
from cart.models              import Cart

class CartTest(TestCase):
    def setUp(self):
        
        Account.objects.create(
            id           = 1,     
            email        = 'user1@naver.com',
            password     = '1q2w3e4r5t@',
            name         = 'user1',
            phone_number = '01077778888'
        )

        Size.objects.create(
            id   = 1,
            name = 'sizeFirst'
        )
        
        Category.objects.create(
            id   = 1,
            name = 'categoryFirst'
        )
        
        Type.objects.create(
            id   = 1,
            name = 'typeFirst'
        )
        
        Product.objects.create(
            id                  = 1,
            name                = "test1product",
            price               = 10000,
            main_img_url        = "http://nike.jpg",
            description_title   = "테스트 타이틀1",
            description_content = "테스트 컨텐트1",
            category_id         = 1,
            type_id             = 1, 
        )
        
        Product.objects.create(
            id                  = 10,
            name                = "test1product",
            price               = 10000,
            main_img_url        = "http://nike.jpg",
            description_title   = "테스트 타이틀1",
            description_content = "테스트 컨텐트1",
            category_id         = 1,
            type_id             = 1, 
        )
        
        Cart.objects.create(
           id         = 1,
           count      = 1,
           account_id = 1,
           size_id    = 1,
           product_id = 1
        )
        self.token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')    

    def tearDown(self):
        Account.objects.all().delete()
        Size.objects.all().delete()
        Category.objects.all().delete()
        Type.objects.all().delete()
        Product.objects.all().delete()
             
    def test_cart_post_success(self):
        client = Client()
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'count'      : 10, 
            'account_id' : 1,
            'product_id' : 10,
            'size_id'    : 1
        }
        response = client.post('/cart', json.dumps(data), **headers, content_type = 'application/json')  
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'CREATE_SUCCESS'})
                    
    def test_cart_post_exist_cart(self):
        client = Client()
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'count'      : 100, 
            'account_id' : 1,
            'product_id' : 1,
            'size_id'    : 1,
        }
        response = client.post('/cart', json.dumps(data), **headers, content_type = 'application/json')  
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_REQUEST'})  
        
    def test_cart_post_key_error(self):
        client = Client()
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'count'     : 1, 
            'account_id' : 1,
            'productt_id' : 1,
            'size_id'    : 1,
        }
        response = client.post('/cart', json.dumps(data), **headers, content_type = 'application/jsons') 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEYS'})
  
    def test_cart_get_success(self):
        client = Client()
        headers = {'HTTP_Authorization' : self.token, 'content_type' : 'application/json'}
        response = client.get('/cart', **headers)

        self.assertEqual(response.json(),{
            'cart_list' :[{
                'cartId' : 1,
                'productId'   : 1,
                'sizeId'       : 1,
                'name'         : "test1product",
                'price'        : 10000,
                'productImage' : "http://nike.jpg",
                'count'        : 1
            }]})        
        self.assertEqual(response.status_code, 200)
        
    def test_cart_patch_not_exist(self):  
        client = Client() 
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'cart_id' : 3,
            'count'   : 2
        }
        response = client.patch('/cart', json.dumps(data), **headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'CART_NOT_EXISTS'})
         
    def test_cart_patch_update_success(self):
        client = Client() 
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'cart_id': 1,
            'count'  : 11
        } 
        response = client.patch('/cart', json.dumps(data), **headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'UPDATE_SUCCESS'})      
    
    def test_cart_patch_update_key_error(self):
        client = Client()       
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'cart_id': 1,
            'countt'  : 4
        } 
        response = client.patch('/cart', json.dumps(data), **headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_KEYS'})      

    def test_cart_delete_success(self):
        client = Client() 
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'cart_id': 1,
        } 
        response = client.delete('/cart', json.dumps(data), **headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'DELETE_SUCCESS'})  
        
    def test_cart_delete_not_exist_cart(self):
        client = Client() 
        headers = {'HTTP_Authorization' : self.token}
        
        data = {
            'cart_id': 100,
        } 
        response = client.delete('/cart', json.dumps(data), **headers, content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message' : 'NOT_EXIST_CART'})          