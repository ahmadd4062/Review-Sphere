# admin.py
from django.contrib import admin
from .models import Blog, Comment, ContactMessage

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(ContactMessage)
