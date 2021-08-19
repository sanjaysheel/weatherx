from django.db import models

# Create your models here.



class Person(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    userslug = models.CharField(max_length=50,unique=True)
    aboutperson = models.CharField(max_length=500,default='',blank=True)
    contact = models.CharField(max_length=15)
    email = models.EmailField(max_length=50,unique=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    aboutprofile = models.CharField(max_length=500, default="", blank=True, null=True)
    photo = models.ImageField(upload_to='profile/image', default="")
    timeStamp1 = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fname+' '+self.lname
    









class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    content = models.TextField()
    def __str__(self):
        return "Name: " +self.name + ' and Email is: ' + self.email

