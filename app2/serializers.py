from rest_framework import serializers
from .models import ReviewAPI
from b_28027.models import Blog  # Import your existing Blog model

class ReviewAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAPI
        fields = '__all__'
