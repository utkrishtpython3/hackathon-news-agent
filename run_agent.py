import json
import boto3
import requests
import os
import datetime
from dotenv import load_dotenv

# Load the secret keys from your .env file
load_dotenv()

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DYNAMO_TABLE_NAME = os.getenv('DYNAMO_TABLE_NAME')
SEARCH_TOPIC = 'artificial intelligence' # You can change this
# ---------------------

comprehend = boto3.client('comprehend') # We aren't using this, but it's fine
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def run_news_agent():
    """
    Main function to fetch, analyze, and store news.
    """
    print(f"--- Starting News Agent for topic: {SEARCH_TOPIC} ---")
    
    # === 1. FETCH NEWS ===
    try:
        url = (
            'https://newsapi.org/v2/top-headlines?'
            f'q={SEARCH_TOPIC}&'
            'pageSize=5&'
            'language=en&'
            f'apiKey={NEWS_API_KEY}'
        )
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        articles = data.get('articles', [])
        
        if not articles:
            print("No articles found for this topic.")
            return
            
        print(f"Fetched {len(articles)} articles.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from NewsAPI: {e}")
        return
    
    # === 2. & 3. ANALYZE & STORE ===
    results = []
    
    for article in articles:
        title = article.get('title')
        article_url = article.get('url')
        source_name = article.get('source', {}).get('name')
        
        if not title:
            continue

        try:
            # --- 2. ANALYZE (Simple Sentiment) ---
            # ⭐ START OF NEW CODE ⭐
            title_lower = title.lower()
            sentiment = 'NEUTRAL' # Default
            
            negative_keywords = ['crash', 'scandal', 'plummets', 'fraud', 'illegal', 'warns', 'risk']
            positive_keywords = ['breakthrough', 'record-high', 'launches', 'successful', 'solves', 'revolutionary']
            
            if any(keyword in title_lower for keyword in negative_keywords):
                sentiment = 'NEGATIVE'
            elif any(keyword in title_lower for keyword in positive_keywords):
                sentiment = 'POSITIVE'
            
            print(f"  > Processing: '{title}'... [Sentiment: {sentiment}]")
            # ⭐ END OF NEW CODE ⭐

            # --- 3. STORE (in DynamoDB) ---
            item_id = article_url 
            iso_timestamp = datetime.datetime.now().isoformat()

            table.put_item(
                Item={
                    'articleId': item_id,
                    'title': title, # Store original title
                    'source': source_name,
                    'topic': SEARCH_TOPIC,
                    'sentiment': sentiment, # <-- ⭐ ADDED THIS LINE ⭐
                    'fetchedAt': iso_timestamp
                }
            )
            
            results.append({'title': title})

        except Exception as e:
            print(f"Error processing article '{title}': {e}")
            
    print(f"\n--- Function complete. Successfully processed and stored {len(results)} articles. ---")
    print("Go check your DynamoDB table!")

# --- This makes the script run when you call it from the command line ---
if __name__ == "__main__":
    if not NEWS_API_KEY or not DYNAMO_TABLE_NAME:
        print("Error: NEWS_API_KEY or DYNAMO_TABLE_NAME not set.")
        print("Please create a .env file with your credentials.")
    else:
        run_news_agent()