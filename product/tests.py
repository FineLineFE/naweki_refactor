import json
from django.test import TestCase, Client
from .models     import Color, ProductColor, Product, Category, Type, ProductSize, Size, SubImageUrl

class ProductListViewTest(TestCase):
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
            main_img_url        = "http://nike2.jpg",
            description_title   = "테스트 타이틀2",
            description_content = "테스트 컨텐트2",
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
        
        
        
class ProductViewTest(TestCase):
    def setUp(self):
        
        category = Category.objects.create(
            id = 1,
            name = "categoryFirst"
        )
        
        type = Type.objects.create(
            id  = 1,
            name = "typeFirst"
        )
        
        product = Product.objects.create(
            id = 1,
            name = "first",
            price = 10000,
            main_img_url = "http://nike.jpg",
            description_title = "타이틀",
            description_content = "컨텐츠",
            category_id = category.id,
            type_id = type.id
        )
        
        color = Color.objects.create(
            id = 1,
            name = "color1"
        )
        
        size = Size.objects.create(
            id = 1,
            name = "size1"
        )
        
        subimgurl = SubImageUrl.objects.create(
            id = 1,
            image_url = "http://nikeimg.jpg",
            product_id = 1
        )
        
    def tearDown(self):
        Product.objects.all().delete()
    
    def test_productlistview_get_success(self):
        client = Client()
        response = self.client.get('/product/1')
        data = {
                "categoryId" : 1,
                "colorId"    : 1,
                "colorName"  : "color1",
                "content"    : "content 임의작성",
                "id"         : 1,
                "imageUrl"   : ["http://nikeimg.jpg"],
                "name"       : "first",
                "price"      : 10000,
                "sizeId"     : 1,
                "sizeName"   : "size1",
                "title"      : "타이틀",
                "color"      : ["color1"],
                "size"       : ["size1"], 
                "typeId"     : 1   
            }
        self.assertEqual(response.json(), {"message" : data})
        self.assertEqual(response.status_code, 200)