from django.db import models

# Create your models here.

class ReviewAPI(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    review_type = models.CharField(max_length=20, choices=[
        ('movie', 'Movie'),
        ('tv_series', 'TV Series')
    ])
    sentiment = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title