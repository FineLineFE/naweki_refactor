from django.db import models

class Account(models.Model):
    
    email        = models.EmailField(max_length = 254, unique = True)
    password     = models.CharField(max_length = 600)
    name         = models.CharField(max_length = 30)
    phone_number = models.CharField(max_length = 50, unique = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "accounts"