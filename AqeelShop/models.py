from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length = 50)
    category = models.CharField(max_length = 100,default = "")
    Subcategory = models.CharField(max_length = 100,default = "")
    price = models.IntegerField(default = 0)
    discription = models.CharField(max_length = 50)
    date_publish = models.DateField()
    images = models.ImageField(upload_to="AqeelShop/images",default = "")

    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100,default = "")
    phone = models.CharField(max_length = 100,default = "")
    desc = models.CharField(max_length = 500,default = "") 

    def __str__(self):
        return self.name 

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.TextField(max_length = 5000)
    amount = models.IntegerField(default = "")
    name = models.CharField(max_length = 100,default = "")
    email = models.CharField(max_length = 100,default = "")
    address = models.CharField(max_length = 500,default = "")     
    city = models.CharField(max_length = 100,default = "")
    state = models.CharField(max_length = 100,default = "")
    zipcode = models.CharField(max_length = 100,default = "")
    phone = models.CharField(max_length = 100,default = "")

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."    


