from django import forms
from .models import ContactMessage, Blog, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg border-2',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg border-2',
                'placeholder': 'you@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-2',
                'rows': 6,
                'placeholder': 'Please describe your inquiry in detail...'
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'message': 'Your Message',
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'review_type', 'content', 'cover_image']  # Added cover_image
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg border-2',
                'placeholder': 'Enter an engaging title for your review'
            }),
            'review_type': forms.Select(attrs={
                'class': 'form-select form-select-lg border-2',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control border-2',
                'rows': 8,
                'placeholder': 'Write your detailed review here...'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Review Title',
            'review_type': 'Review Type',
            'content': 'Review Content',
        }
        help_texts = {
            'title': 'Make it catchy and descriptive!',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 4,
                'style': 'border-radius: 10px;'
            }),
        }
        labels = {
            'content': 'Add your comment',
        }

    
class SentimentAnalysisForm(forms.Form):
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter your movie review here...',
            'style': 'background-color: #222222; color: #e0e0e0; border-color: #6a11cb;'  # Fixed: added missing }
        }),
        label='Movie Review',
        max_length=1000
    )
    
    def clean_review_text(self):
        text = self.cleaned_data.get('review_text', '').strip()
        return text