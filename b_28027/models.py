from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    REVIEW_TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Series', 'TV Series'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=20,choices=REVIEW_TYPE_CHOICES)
    cover_image = models.ImageField(
        upload_to='blog_covers/',
        blank=True,
        null=True,
        help_text='Upload a cover image for your review'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.review_type})"


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} ({self.email})'
