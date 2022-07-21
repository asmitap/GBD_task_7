from django.db import models

# Create your models here.
class Scheme(models.Model):
    schema_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.schema_name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    parent_xpath = models.CharField(max_length=200)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_name
    
class Content(models.Model):
    field_name = models.CharField(max_length=100)
    xpath = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.field_name
    