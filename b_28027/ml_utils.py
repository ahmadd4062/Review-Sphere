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
        """Load the trained model from pickle file"""
        # Try multiple possible locations
        possible_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sentiment_model.pkl'),
            os.path.join(settings.BASE_DIR, 'b_28027', 'sentiment_model.pkl'),
            os.path.join(settings.BASE_DIR, 'sentiment_model.pkl'),
        ]
        
        for model_path in possible_paths:
            print(f"Looking for model at: {model_path}")
            if os.path.exists(model_path):
                try:
                    with open(model_path, 'rb') as f:
                        model_data = pickle.load(f)
                    
                    self.model = model_data['model']
                    self.vectorizer = model_data['vectorizer']
                    self.classes = model_data['classes']
                    print(f"✅ Sentiment Analysis Model loaded from: {model_path}")
                    return
                except Exception as e:
                    print(f"❌ Error loading from {model_path}: {str(e)}")
                    continue
        
        print("❌ Model not found in any location")
        self.model = None
    
    # Rest of your methods remain the same...
    def preprocess_text(self, text):
        """Preprocess text for prediction"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        stemmer = PorterStemmer()
        words = text.split()
        stop_words = set(stopwords.words('english'))
        words = [stemmer.stem(word) for word in words if word not in stop_words]
        return ' '.join(words)
    
    def predict_sentiment(self, review_text):
        """Predict sentiment of a review"""
        if not self.model:
            return {
                "error": "Model not loaded",
                "sentiment": "unknown",
                "confidence": 0,
                "probabilities": {"negative": 50, "positive": 50}
            }
        
        processed_text = self.preprocess_text(review_text)
        if not processed_text or len(processed_text.split()) < 2:
            return {
                "sentiment": "neutral",
                "confidence": 50,
                "probabilities": {"negative": 50, "positive": 50},
                "note": "Text too short for accurate analysis"
            }
        
        vectorized_text = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(vectorized_text)[0]
        probabilities = self.model.predict_proba(vectorized_text)[0]
        
        return {
            'sentiment': self.classes[prediction] if prediction < len(self.classes) else 'unknown',
            'confidence': float(max(probabilities)) * 100,
            'probabilities': {
                'negative': float(probabilities[0]) * 100,
                'positive': float(probabilities[1]) * 100
            }
        }
    
    def batch_predict(self, review_list):
        """Predict sentiment for multiple reviews"""
        return [{'review': review, 'result': self.predict_sentiment(review)} for review in review_list]
    
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