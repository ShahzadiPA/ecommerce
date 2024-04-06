from django.db import models
from bcart.models import Product
# Create your models here.
class Oncart(models.Model):
    carts_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Oncart'
        ordering = ['date_added']
    def __str__(self):
        return '{}'.format(self.carts_id)
class CartItem(models.Model):
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    oncart=models.ForeignKey(Oncart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    class Meta:
        db_table='CartItem'
    def sub_total(self):
        return self.products.price * self.quantity

    def __str__(self):
        return '{}'.format(self.products)
