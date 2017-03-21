from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager


class AUser(AbstractUser):
    USERNAME_FIELD = 'username'
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ('email','password','first_name','last_name',)

class RepairerManager(BaseUserManager):
    def create_user(self, email, password=None, fname=None, lname=None,uname=None,phone=None,secretque=None,secretans=None,cnic=None,lon='1.0',lat='1.0',shopid=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=RepairerManager.normalize_email(email),
            first_name=fname,
            last_name=lname,
            username=uname,
            contactNo=phone,
            secretQuestion=secretque,
            secretAnswer=secretans,
            cnic=cnic,
            longitude=lon,
            latitude=lat,
            shopid=shopid
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class Shop(models.Model):
    id=models.IntegerField(default=0,serialize=False, verbose_name='ID')
    #username = models.ForeignKey(Repairer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,primary_key=True)


class Repairer(AUser):
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15)
    contactNo = models.CharField(max_length=12)
    longitude = models.FloatField(max_length=10,null=True)
    latitude = models.FloatField(max_length=10,null=True)
    secretQuestion = models.CharField(max_length=400)
    secretAnswer = models.CharField(max_length=250)
    shopid=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True)
    objects = RepairerManager()


class Expertise(models.Model):
    username = models.ForeignKey(Repairer, on_delete=models.CASCADE)
    workCategory = models.CharField(max_length=200)

class RepairerRating(models.Model):
    r_username = models.ForeignKey(Repairer, on_delete=models.CASCADE)
    c_username=models.CharField(max_length=100,default="null")
    rating=models.FloatField()
    reviews=models.CharField(max_length=1000)

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, fname=None, lname=None,uname=None,phone=None,secretque=None,secretans=None,cnic=None,lon='1.0',lat='1.0'):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=CustomerManager.normalize_email(email),
            first_name=fname,
            last_name=lname,
            username=uname,
            contactNo=phone,
            secretQuestion=secretque,
            secretAnswer=secretans,
            longitude=lon,
            latitude = lat,
            cnic=cnic
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user




class Customer(AUser):
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cnic = models.CharField(max_length=15)
    contactNo = models.CharField(max_length=12)
    longitude = models.FloatField(max_length=10, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    secretQuestion = models.CharField(max_length=400)
    secretAnswer = models.CharField(max_length=250)
 #   contactNo = models.CharField(max_length=12)
    objects = CustomerManager()



class CustomerRating(models.Model):
    c_username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating=models.FloatField()
    r_username = models.CharField(max_length=100,default="null")
    reviews=models.CharField(max_length=1000)


class Favourites(models.Model):
    c_username = models.ForeignKey(Customer, on_delete=models.CASCADE)
    r_username = models.CharField(max_length=100)


