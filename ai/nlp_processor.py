import http.client
import json
import os
import urllib.parse  # Needed for URL encoding
from dotenv import load_dotenv

"""
# Load environment variables
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')  

async def get_ai_response(message, user_id):
    #Get AI-powered response using the free ChatGPT API on RapidAPI.
    
    conn = http.client.HTTPSConnection("free-chatgpt-api.p.rapidapi.com")
    
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': "free-chatgpt-api.p.rapidapi.com"
    }
    
    try:
        # URL encode the message to avoid issues with spaces, symbols, etc.
        encoded_message = urllib.parse.quote(message)
        request_url = f"/chat-completion-one?prompt={encoded_message}"

        # Make the request
        conn.request("GET", request_url, headers=headers)
        res = conn.getresponse()  # ❌ No need to 'await' this (it's synchronous)
        data = res.read().decode("utf-8")
        conn.close()  # ✅ Always close the connection after use
        
        # Parse the JSON response
        response_data = json.loads(data)
        
        # Extract the AI response 
        if "answer" in response_data:
            return response_data["answer"]
        elif "response" in response_data:
            return response_data["response"]
        else:
            return "🤖 Sorry, I couldn't process that. Try again."
    
    except Exception as e:
        print(f"⚠️ Error in AI response: {e}")
        return "⚠️ AI is currently unavailable. Please try again later."
    """

import os
import json
import http.client
#import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MYTELEBOT_TOKEN = os.getenv('MYTELEBOT_TOKEN')  # Store your API key in .env file

async def get_ai_response(message, user_id):
    """Get AI-powered response using Hugging Face's BlenderBot API."""

    conn = http.client.HTTPSConnection("api-inference.huggingface.co")

    headers = {
        'Authorization': f'Bearer {MYTELEBOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Prepare request payload
        payload = json.dumps({"inputs": message})
        
        # Make the request
        conn.request("POST", "/models/facebook/blenderbot-3B", body=payload, headers=headers)
        res = conn.getresponse()  # ❌ No need to 'await' this (it's synchronous)
        data = res.read().decode("utf-8")
        conn.close()  # ✅ Always close the connection
        
        # Parse JSON response
        response_data = json.loads(data)

        # Extract AI response
        if isinstance(response_data, list) and "generated_text" in response_data[0]:
            return response_data[0]["generated_text"]
        elif "error" in response_data:
            return f"⚠️ AI Error: {response_data['error']}"
        else:
            return "🤖 Sorry, I couldn't process that. Try again."
    
    except Exception as e:
        print(f"⚠️ Error in AI response: {e}")
        return "⚠️ AI is currently unavailable. Please try again later."

#Sentiment Analysis for Engagement
import requests
import json

load_dotenv()
API_VERVE_KEY = os.getenv('API_VERVE_KEY')

async def analyze_sentiment(text):
    """Analyze the sentiment of a message using APIVerve."""
    url = "https://api.apiverve.com/v1/sentimentanalysis"
    
    headers = {
        "x-api-key": API_VERVE_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {"text": text}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()
        return data.get("sentiment", "neutral")  # Return sentiment (positive, neutral, negative)
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Sentiment analysis error: {e}")
        return "neutral"


