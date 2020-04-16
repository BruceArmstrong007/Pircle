from django.db import models
# Create your models here.
class user(models.Model):
    email = models.CharField( max_length=50, unique=True, null=False)
    password = models.CharField( max_length=32, null=False)
    otp = models.CharField(max_length=15,null = True)
    active = models.CharField(max_length = 15, choices = [('active','active'),('In-active','In-active')],default = "In-active")
    def __str__(self):
        return self.email
    