from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Shop(models.Model):
    category_choices = [
        ('fast-food','Fast Food'),
        ('cafe','Cafe'),
        ('fine-dining','Fine Dining'),
        ('light-meals','Light Meals'),
        ('desserts','Desserts'),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=category_choices, default='other')
    location = models.CharField(max_length=50)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def avg_rating(self):
        reviews = self.reviews.all()
        total = sum([review.rating for review in reviews])
        return round(total/reviews.count(),1) if reviews.count()>0 else 0
    

class Review(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reviews')
    # related_name allows us to access reviews from a shop instance using shop.reviews.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upv = models.IntegerField(default=0)
    dnv = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted', blank=True)
    downvoted_by = models.ManyToManyField(User, related_name='downvoted', blank=True)
    def __str__(self):
        return f"{self.user.username} → {self.shop.name} ({self.rating}⭐)"
    def total_votes(self):
        return self.upv - self.dnv