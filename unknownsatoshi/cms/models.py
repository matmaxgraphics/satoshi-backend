import uuid
from django.db import models
from userprolog.models import User
from django.urls import reverse
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save
from ckeditor_uploader.fields import RichTextUploadingField
from userprolog.models import User



today = datetime.now().date()

class ProductCategory(models.Model):
    name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class Cms(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    entry = models.TextField(null=True, blank=True)
    stoploss = models.TextField(null=True, blank=True)
    tp_target = models.IntegerField(default=0, null=True, blank=True)
    tp_achieved = models.IntegerField(default=0, null=True, blank=True)
    profit = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    courses = models.TextField(null=True, blank=True)
    course_link = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.png", upload_to="course_images/")

    def __str__(self):
        return self.courses
        

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.TextField(null=True, blank=True)
    product_link = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    featured_image = models.ImageField(null=True, blank=True, default="default.png", upload_to="product_images/")
   
    def __str__(self):
        return self.product_name


class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=True)
    post = RichTextUploadingField()
    featured_stories = models.BooleanField(default=False)
    latest_news = models.BooleanField(default=False)
    latest_articles = models.BooleanField(default=False)
    featured_image = models.ImageField(null=True, blank=True, default="default.png", upload_to="blog_images/")
    premium = models.BooleanField(default=False)
    home_page = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_on', 'updated_on']

    def __str__(self):
        return self.title

    def snippet(self):
        return self.post[:200]

    def home_snippet(self):
        return self.post[:200]

    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"slug": self.slug})
    

#subscription plan for premium blog views 
class Plan(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    desc = models.TextField()
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    discount= models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("created_on",)

    def __str__(self):
        return self.title


# this saves the subscriptin record
class SubscriptionHistory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=False, blank=False)
    full_name = models.CharField(max_length=200, blank=False)
    phone_no = models.CharField(max_length=11, unique=False, blank=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, default='monthly plan')
    amount_paid = models.IntegerField(default=0)
    reference = models.CharField(max_length=200, unique=True, blank=False)
    transaction_id = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    start_date = models.DateField(default=today)
    expiry_date = models.DateField(default=None)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=SubscriptionHistory)
def update_activeness(sender, instance, *args, **kwargs):
    if instance.expiry_date <= today:
        instance.active = False
    else:
        instance.active = True
    

class Newsletter(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email