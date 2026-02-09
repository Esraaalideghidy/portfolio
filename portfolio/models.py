from django.db import models
from datetime import date
from .services import convert_to_webp



class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    sub_description = models.TextField(null=True, blank=True)
    sub_description2 = models.TextField(null=True, blank=True)
    


    def __str__(self):
        return self.title
    

class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    birthday = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255, null=True)
    cv = models.FileField(upload_to='cv/', null=True)
    city = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=50, null=True)
    freelancer = models.CharField(max_length=50, null=True)


    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def calculated_age(self):
        if self.birthday:
            today = date.today()
            return today.year - self.birthday.year - (
                (today.month, today.day) < (self.birthday.month, self.birthday.day)
            )
        return None



    

class Skill(models.Model):
    name = models.CharField(max_length=100) 
    level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=50, help_text="Bootstrap icon class, e.g., bi bi-code-slash",blank=True, null=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class PortfolioItem(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='portfolio_items/', null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PortfolioImage(models.Model):
    portfolio_item = models.ForeignKey(PortfolioItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.portfolio_item.title}"