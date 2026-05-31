from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ReviewAPI
from b_28027.models import Blog 
from .serializers import ReviewAPISerializer

class ReviewAPIView(APIView):
    # GET: Fetch all API reviews
    def get(self, request):
        reviews = ReviewAPI.objects.all()
        serializer = ReviewAPISerializer(reviews, many=True)
        return Response(serializer.data)

    # POST: Add a new review via API
    def post(self, request):
        serializer = ReviewAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
