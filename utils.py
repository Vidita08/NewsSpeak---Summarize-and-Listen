from textblob import TextBlob
from gtts import gTTS
import os
from collections import Counter
from transformers import pipeline

class NewsAnalyzer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"

    def extract_topics(self, text):
        blob = TextBlob(text)
        nouns = blob.noun_phrases
        return list(set([noun.title() for noun in nouns]))[:5]

    def summarize_text(self, text, max_length=130, min_length=30):
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text[:200] + "..."

    def generate_english_audio(self, text, output_file="output.mp3"):
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_file)
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False

    def analyze_articles(self, articles):
        results = []
        sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
        
        for article in articles:
            sentiment = self.analyze_sentiment(article['description'])
            summary = self.summarize_text(article['description'])
            topics = self.extract_topics(article['description'])
            
            sentiment_distribution[sentiment] += 1
            
            results.append({
                "Title": article['title'],
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics
            })
            
        return results, sentiment_distribution