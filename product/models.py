from django.db       import models

class Product(models.Model):
    name                = models.CharField(max_length = 100)
    price               = models.DecimalField(max_digits = 10, decimal_places = 2)
    main_img_url        = models.URLField()
    description_title   = models.CharField(max_length = 100)
    description_content = models.CharField(max_length = 1000)
    category            = models.ForeignKey('Category', on_delete = models.CASCADE)
    type                = models.ForeignKey('Type', on_delete = models.CASCADE)
    color               = models.ManyToManyField('Color', through = 'ProductColor')
    size                = models.ManyToManyField('Size', through = 'ProductSize')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products" 

class Category(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = "categories"

class Type(models.Model):
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "types"
        
class Color(models.Model):
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = "colors"

class ProductColor(models.Model):
    color   = models.ForeignKey('color', on_delete = models.CASCADE)
    product = models.ForeignKey('product', on_delete = models.CASCADE)

    class Meta:
        db_table = "products_colors"

class Size(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sizes"

class ProductSize(models.Model):
    size    = models.ForeignKey('size', on_delete = models.CASCADE)
    product = models.ForeignKey('product', on_delete = models.CASCADE)

    class Meta:
        db_table = "products_sizes"
        
class SubImageUrl(models.Model):
    image_url     = models.URLField()
    product       = models.ForeignKey('product', on_delete = models.CASCADE)

    def __str__(self):
        return self.image_url

    class Meta:
        db_table = "sub_image_urls"