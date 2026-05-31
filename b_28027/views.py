from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Blog, Comment, ContactMessage 
from .forms import SignupForm, LoginForm, ContactForm, BlogForm, CommentForm, SentimentAnalysisForm
from .ml_utils import sentiment_analyzer
from app2.models import ReviewAPI 

# Signup view
def signup_view(request):  
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Home Page - List all blogs
def home_view(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blogs': blogs})

# Blog Detail Page
def blog_detail_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()
    
    comments = blog.comments.all().order_by('-created_at')
    return render(request, 'blog_detail.html', {
        'blog': blog, 
        'comments': comments,
        'form': form
    })

# Create Blog
@login_required
def create_blog_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog post created successfully!")
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

# Update Blog
@login_required
def update_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Only author can edit
    if blog.author != request.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect('home')
    
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'update_blog.html', {'form': form, 'blog': blog})

# About page
def about_view(request):
    return render(request, 'about.html')

# Contact page 
def contact_view(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            success = True
            # Reset form after successful submission
            form = ContactForm()
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form, 'success': success})

# Sentiment Analysis View (ML Integration)
@login_required
def sentiment_analysis_view(request):

    result = None
    form = SentimentAnalysisForm()
    
    if request.method == 'POST':
        form = SentimentAnalysisForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review_text']
            
            # Get prediction from ML model
            prediction = sentiment_analyzer.predict_sentiment(review_text)
            
            if 'error' in prediction:
                messages.error(request, prediction['error'])
            else:
                result = {
                    'review': review_text,
                    'sentiment': prediction['sentiment'],
                    'confidence': prediction['confidence'],
                    'negative_prob': prediction['probabilities']['negative'],
                    'positive_prob': prediction['probabilities']['positive']
                }
                messages.success(request, f"Analysis complete! Sentiment: {prediction['sentiment'].title()}")
    
    return render(request, 'ml_sentiment.html', {
        'form': form,
        'result': result,
        'title': 'Sentiment Analysis'
    })

    
# In your main app's views.py

def dashboard_view(request):
    # Get data from main app
    blogs = Blog.objects.all()[:5]  # Latest 5 blogs
    
    # Get data from API app
    api_reviews = ReviewAPI.objects.all()[:5]  # Latest 5 API reviews
    
    context = {
        'blogs': blogs,
        'api_reviews': api_reviews,
        'total_blogs': Blog.objects.count(),
        'total_api_reviews': ReviewAPI.objects.count(),
    }
    
    return render(request, 'dashboard.html', context)