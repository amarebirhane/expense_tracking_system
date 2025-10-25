# backend/app/services/ai_categorization.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from typing import List, Dict

# Simulated trained model - in real, train on user data
class SimpleCategorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        # Dummy training data
        self.categories = ['travel', 'meals', 'office_supplies', 'other']
        self.train_data = [
            ("flight to NY", 'travel'),
            ("lunch meeting", 'meals'),
            ("pens and paper", 'office_supplies'),
            ("bus fare", 'travel'),
            ("dinner", 'meals'),
            ("printer ink", 'office_supplies')
        ]
        X = self.vectorizer.fit_transform([text for text, _ in self.train_data])
        y = [cat for _, cat in self.train_data]
        self.model.fit(X, y)

    def categorize(self, notes: str) -> str:
        if not notes:
            return 'other'
        X = self.vectorizer.transform([notes])
        pred = self.model.predict(X)[0]
        return pred

categorizer = SimpleCategorizer()