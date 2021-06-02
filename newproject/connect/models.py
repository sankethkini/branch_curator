from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now


class Member(models.Model):
    mid=models.CharField(primary_key=True,max_length=10)
    name=models.CharField(max_length=15)
    contact=models.CharField(max_length=10,default=None)
    email=models.EmailField(default=None)
    dept=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    
    def __str__(self):
        return self.mid


class Project(models.Model):
    pid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=150)
    time=models.IntegerField(default=30)
    starttime=models.DateField(default=now)
    projshortdesc=models.TextField(default=None)
    field=models.CharField(max_length=20,default=None)
    number_of_people=models.IntegerField()
    techstack=models.CharField(max_length=50,default="programming")
    created_by=models.ManyToManyField(Member)
    
    def __str__(self):
        return self.name+str(self.pid)
    
class Blog(models.Model):
    bid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=150)
    body=models.TextField()
    field=models.CharField(max_length=20,default=None)
    created_by=models.ManyToManyField(Member)
    created_at=models.DateField(default=now)
    def __str__(self):
        return self.title+str(self.bid)


class userProfile(models.Model):
    id=models.OneToOneField(Member,on_delete=models.RESTRICT,primary_key=True)
    projdata=models.BinaryField(default=None)
    blogdata=models.BinaryField(default=None)

    def __str__(self):
        return self.id.name
