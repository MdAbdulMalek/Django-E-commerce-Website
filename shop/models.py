from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 60, default = "")
    sub_category = models.CharField(max_length = 60, default = "")
    price = models.IntegerField(default = 0)
    desc = models.CharField(max_length = 300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = "shop/images", default = "")

    def __str__(self):
        return self.product_name


class Contract(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80, default="")
    phone = models.CharField(max_length=80, default="")
    desc = models.CharField(max_length=800, default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=6000)
    amount=models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=111, default="")

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class User(models.Model):
    user_id= models.AutoField(primary_key=True)
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=80)
    username= models.CharField(max_length=100)
    password= models.CharField(max_length=50)

    def __str__(self):
        return self.username
