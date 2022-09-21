
from random import choices
from django.db import models
from django.contrib import admin
from django import forms
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class Tag(models.Model):
    caption=models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    First_name=models.CharField(max_length=100)
    Last_name=models.CharField(max_length=100)
    email_address=models.EmailField(max_length=254)

    def full_name(self):
        return f"{self.First_name} {self.Last_name}"
    
    def __str__(self) :
        return self.full_name()



class Post(models.Model):
    title=models.CharField(max_length=150)
    excerpt=models.CharField(max_length=200, blank=True)
    image=models.ImageField(upload_to="data",null=True)
    date=models.DateField(auto_now=True)
    slug=models.SlugField(unique=True)
    content=RichTextField(config_name='awesome_ckeditor')
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")
    tags=models.ManyToManyField(Tag) 

    def __str__(self):
        return self.title
    


class PostAdmin(admin.ModelAdmin):
    list_filter=("author","tags","date",)
    list_display=("title","date","author",)
    prepopulated_fields={"slug":["title"]}

class Comment(models.Model):
    user_name=models.CharField(max_length=120)
    user_email=models.EmailField()
    text=models.TextField(max_length=400)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

class CommentAdmin(admin.ModelAdmin):
    list_display=("user_name","post")

class Product(models.Model):
    name=models.CharField(max_length=850)
    price=models.FloatField()
    description=models.TextField()
    imglink=models.CharField(max_length=850)
    taghchelink=models.CharField(default="",max_length=850)

    def __str__(self):
        return f"Book name:{self.name}(Price:{self.price})"

class Order(models.Model):
    first_name=models.CharField(max_length=400,blank=False)
    last_name=models.CharField(max_length=600,blank=False)
    address=models.CharField(max_length=600,blank=False)
    city=models.CharField(max_length=200,blank=False)
    mobile=models.IntegerField(default=None,blank=False)
    postcode=models.IntegerField(default=None,blank=False)
    email=models.EmailField(default=None,blank=False)
    items=models.TextField(default=None,blank=False)
    authority=models.CharField(default="",blank=True,max_length=600)
    status=models.CharField(default="",blank=True,max_length=600)

    
    def clean(self):
      if self.name == '':
        raise ValidationError('جاهای خالی را پرکنید')

class OrderAdmin(admin.ModelAdmin):
    list_display = ("email","first_name")