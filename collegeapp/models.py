from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserMember(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_address = models.CharField(max_length=255)
    user_gender= models.CharField(max_length=255)
    user_mobile= models.CharField(max_length=255)
    user_photo=models.ImageField(upload_to='image/',null=True)

    #def __str__(self):
        #return self.user.username

class course(models.Model):
    course_name=models.CharField(max_length=255)
    fee = models.IntegerField()

    def __str__(self):
        return self.course_name

class student(models.Model):
    course=models.ForeignKey(course,on_delete=models.CASCADE,null=True)
    std_name=models.CharField(max_length=255)
    std_address=models.CharField(max_length=255)
    std_age=models.IntegerField()
    std_date=models.DateField()

    def __str__(self):
        return self.std_name