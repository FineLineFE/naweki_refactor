import json
from django.test import TestCase, Client
from .models     import Color, ProductColor, Product, Category, Type, ProductSize, Size, SubImageUrl

class ProductListViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        
        category = Category.objects.create(
            id = 1,
            name = "categoryFirst"
        )
        
        type = Type.objects.create(
            id = 1,
            name = "typeFirst"
        )
        
        Product.objects.create(
            id                  = 1,
            name                = "test1product",
            price               = 10000,
            main_img_url        = "http://nike.jpg",
            description_title   = "테스트 타이틀1",
            description_content = "테스트 컨텐트1",
            category_id         = category.id,
            type_id             = type.id, 
        )
        Product.objects.create(
            id                  = 2,
            name                = "test1product",
            price               = 10000,
            main_img_url        = "http://nike.jpg",
            description_title   = "테스트 타이틀1",
            description_content = "테스트 컨텐트",
            category_id         = category.id,
            type_id             = type.id, 
        )
        
    def tearDown(self):
        Product.objects.all().delete() 
        
    def test_productlistview_get_success(self):
        client = Client() 
        
        response = self.client.get('/product') 
        product_list =[
                {
                "id"                 : product.id,
                "productImage"       : product.main_img_url,
                "name"               : product.name,
                "price"              : 10000,
                } for product in Product.objects.all()
            ]
        self.assertEqual(response.json(), {"message": product_list})
        self.assertEqual(response.status_code, 200)