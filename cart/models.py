from django.db      import models
from account.models import Account
from product.models import Product, Size

class Cart(models.Model):
    
    count      = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account    = models.ForeignKey('account.Account', on_delete = models.CASCADE)
    size       = models.ForeignKey('product.Size', on_delete = models.CASCADE, null = True)
    product    = models.ForeignKey('product.Product', on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "carts"