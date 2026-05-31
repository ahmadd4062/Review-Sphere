import pickle
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
from django.conf import settings

# Download NLTK data (run once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.classes = None
        self.load_model()
        
    def load_model(self):
        """Load the trained model from pickle file in app folder"""
        # Get the absolute path to the app directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(app_dir, 'sentiment_model.pkl')
        
        print(f"Looking for model at: {model_path}")
        
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.classes = model_data['classes']
            print("✅ Sentiment Analysis Model loaded successfully!")
            
        except FileNotFoundError:
            print(f"❌ Model file not found at {model_path}")
            print("Please download sentiment_model.pkl from Colab and place it in the app/ folder")
            print("Current directory contents:", os.listdir(app_dir))
            self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self.model = None
    
    def preprocess_text(self, text):
        """Preprocess text for prediction"""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenization and stemming
        stemmer = PorterStemmer()
        words = text.split()
        # Remove stopwords and stem
        stop_words = set(stopwords.words('english'))
        words = [stemmer.stem(word) for word in words if word not in stop_words]
        
        return ' '.join(words)
    
    def predict_sentiment(self, review_text):
        """Predict sentiment of a review"""
        if not self.model:
            return {
                "error": "Model not loaded. Please check if sentiment_model.pkl exists in the app folder.",
                "sentiment": "unknown",
                "confidence": 0,
                "probabilities": {"negative": 50, "positive": 50}
            }
        
        # Preprocess text
        processed_text = self.preprocess_text(review_text)
        
        if not processed_text or len(processed_text.split()) < 2:
            return {
                "sentiment": "neutral",
                "confidence": 50,
                "probabilities": {"negative": 50, "positive": 50},
                "note": "Text too short for accurate analysis"
            }
        
        # Vectorize
        vectorized_text = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(vectorized_text)[0]
        probabilities = self.model.predict_proba(vectorized_text)[0]
        
        result = {
            'sentiment': self.classes[prediction] if prediction < len(self.classes) else 'unknown',
            'confidence': float(max(probabilities)) * 100,
            'probabilities': {
                'negative': float(probabilities[0]) * 100,
                'positive': float(probabilities[1]) * 100
            }
        }
        
        return result
    
    def batch_predict(self, review_list):
        """Predict sentiment for multiple reviews"""
        results = []
        for review in review_list:
            result = self.predict_sentiment(review)
            results.append({
                'review': review,
                'result': result
            })
        return results

    def get_model_info(self):
        """Get information about the loaded model"""
        if not self.model:
            return "Model not loaded"
        
        return {
            'model_type': type(self.model).__name__,
            'classes': self.classes,
            'features': self.vectorizer.get_feature_names_out().shape[0] if hasattr(self.vectorizer, 'get_feature_names_out') else 'Unknown',
            'status': 'Loaded'
        }

# Create a global instance
sentiment_analyzer = SentimentAnalyzer()