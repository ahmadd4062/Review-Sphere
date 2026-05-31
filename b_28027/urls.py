from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('blog/<int:blog_id>/', views.blog_detail_view, name='blog_detail'),
    path('blog/create/', views.create_blog_view, name='create_blog'),
    path('blog/<int:blog_id>/update/', views.update_blog_view, name='update_blog'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('sentiment-analysis/', views.sentiment_analysis_view, name='sentiment_analysis'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]


