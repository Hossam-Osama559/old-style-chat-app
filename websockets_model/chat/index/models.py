from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class msg(models.Model):

    content=models.CharField(max_length=100)

    seneder=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    reciever_name=models.CharField(max_length=100,default="hossam")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciever")




class friends(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")

    friend=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_friend")



class notifications(models.Model):

    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="x")

    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="y")

    noti_type=models.BooleanField(default=0)   #0 means add friend    and 1 means that the user respond 

    res_type=models.BooleanField(default=0)    #0 means descard and 1 means ok

    