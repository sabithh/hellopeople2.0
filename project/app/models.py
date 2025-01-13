from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class RegistrationModelManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class registrationmodel(models.Model):
    name=models.CharField(max_length=30)
    username=models.CharField(primary_key=True,max_length=20)
    email=models.EmailField(unique=True)
    phone=models.IntegerField()
    bio=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=30)
    photo=models.FileField(null=True)
    last_login = models.DateTimeField(auto_now=True)  # Add this line
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RegistrationModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_email_field_name(self):
        return 'email'

class employemodel(models.Model):
    name=models.CharField(max_length=20)
    bio=models.CharField(max_length=100)
    phone=models.IntegerField()
    photo=models.FileField()
    photo1=models.FileField()
    email=models.EmailField()
    city=models.CharField(max_length=50)
    rate=models.IntegerField()
    password=models.CharField(max_length=30)
    activation=models.BooleanField(default=False)
class adminmodel(models.Model):
    adid=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=20)

class slotmodel(models.Model):
    stname=models.CharField(max_length=100)
    stphoto=models.FileField()
    stphoto2 = models.FileField()
    stphoto3= models.FileField()
    stdeteals=models.CharField(max_length=500)

class Appointment(models.Model):
    employee=models.ForeignKey(employemodel,on_delete=models.CASCADE)
    date = models.DateTimeField()
    location=models.CharField(max_length=80)
    services=models.ForeignKey(slotmodel,on_delete=models.CASCADE)
    user=models.ForeignKey(registrationmodel,on_delete=models.CASCADE)
    activation=models.BooleanField(default=False)
    payment=models.BooleanField(default=False)

class raiseslotmodel(models.Model):
    stname=models.CharField(max_length=100)
    username=models.CharField(max_length=50)
    userphoto = models.FileField(null=True)
    stdeteals=models.CharField(max_length=500)
    city= models.CharField(max_length=30)
    splocation= models.CharField(max_length=100,null=True)
