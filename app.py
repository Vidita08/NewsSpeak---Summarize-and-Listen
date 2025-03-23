import streamlit as st
from api import NewsAPI
from utils import NewsAnalyzer
import json
import streamlit as st
from api import NewsAPI
from utils import NewsAnalyzer
import json
from collections import Counter

# Initialize API and Analyzer
API_KEY = "[API-KET]"
news_api = NewsAPI(API_KEY)
analyzer = NewsAnalyzer()

def main():
    st.title("Company News Analysis and Sentiment Report")
    
    # User input
    company_name = st.text_input("Enter Company Name:", "Tesla")
    
    if st.button("Analyze"):
        # Fetch news
        news_data = news_api.get_company_news(company_name)
        
        if news_data and news_data['articles']:
            articles = news_data['articles'][:10]  # Get first 10 articles
            
            # Analyze articles
            results, sentiment_distribution = analyzer.analyze_articles(articles)
            
            # Create final report
            report = {
                "Company": company_name,
                "Articles": results,
                "Comparative Sentiment Score": {
                    "Sentiment Distribution": sentiment_distribution,
                    "Coverage Differences": analyze_coverage_differences(results),
                    "Topic Overlap": analyze_topic_overlap(results)
                }
            }
            
            # Display results
            display_results(report)
            
            # Generate Hindi audio summary
            generate_audio_summary(report)
        else:
            st.error("No news articles found or API error occurred.")

def analyze_coverage_differences(results):
    differences = []
    if len(results) >= 2:
        differences.append({
            "Comparison": f"Article 1 focuses on {', '.join(results[0]['Topics'])}, "
                         f"while Article 2 covers {', '.join(results[1]['Topics'])}",
            "Impact": "Different aspects of company coverage provide diverse perspectives."
        })
    return differences

def analyze_topic_overlap(results):
    all_topics = [topic for article in results for topic in article['Topics']]
    common_topics = [topic for topic, count in Counter(all_topics).items() if count > 1]
    
    return {
        "Common Topics": common_topics,
        "Unique Topics": list(set(all_topics) - set(common_topics))
    }

def display_results(report):
    st.header("Analysis Results")
    
    # Display articles
    for idx, article in enumerate(report["Articles"]):
        st.subheader(f"Article {idx + 1}")
        st.write(f"Title: {article['Title']}")
        st.write(f"Summary: {article['Summary']}")
        st.write(f"Sentiment: {article['Sentiment']}")
        st.write(f"Topics: {', '.join(article['Topics'])}")
        st.write("---")
    
    # Display sentiment distribution
    st.subheader("Sentiment Distribution")
    st.write(report["Comparative Sentiment Score"]["Sentiment Distribution"])

def generate_audio_summary(report):
    if report["Articles"] and len(report["Articles"]) > 0:
        # Take the first article's summary
        first_article = report["Articles"][0]
        
        # Create a more detailed summary in English
        summary_text = f"News about {report['Company']}: {first_article['Summary']}"
        
        if analyzer.generate_english_audio(summary_text):
            st.audio("output.mp3")
            st.write("Audio Summary Generated")
        else:
            st.error("Error generating audio summary")
    else:
        st.error("No articles available for audio summary")

if __name__ == "__main__":
    main()
