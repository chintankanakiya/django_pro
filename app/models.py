from django.db import models

# Create your models here.
class User(models.Model):
    Fullname = models.CharField(max_length=50)
    Username = models.CharField(max_length=50)
    Email = models.EmailField(max_length=30)
    Password = models.CharField(max_length=16)

class Category(models.Model):
    cname = models.CharField(max_length=1000)
    def __str__(self):
        return self.cname
    

# class Subcategory(models.Model):
#     cname = models.ForeignKey(Category,on_delete=models.CASCADE)
#     Subcategory = models.CharField(max_length=1000)
        
class Product(models.Model):
    cname = models.ForeignKey(Category,on_delete=models.CASCADE)
    p_name = models.CharField(max_length=200)
    p_price = models.IntegerField()
    p_image = models.ImageField(upload_to='img')
    p_discription = models.CharField(max_length=1000)
    styleno=models.CharField(max_length=6,null=True)
    BottomThickness = models.CharField(max_length=20,null=True)
    TopThickness = models.CharField(max_length=20,null=True)
    TopHeight = models.CharField(max_length=20,null=True)
    TotalWeight = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.p_name

class Cart(models.Model):
    Prodect = models.ForeignKey(Product,on_delete=models.CASCADE)        
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity =models.IntegerField()
    subtotal = models.IntegerField()

class Detail(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    pno = models.IntegerField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    contry = models.CharField(max_length=100)

Bar =(('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Delivered','Delivered'))
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    det = models.ForeignKey(Detail,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    orderstatus=models.CharField(choices=Bar,max_length=50,default='Pending')
    qyantity=models.IntegerField()
    total=models.IntegerField()
     