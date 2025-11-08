#!/usr/bin/env python3
"""
Test script to check available Claude models in GitHub Models API
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Get GitHub token
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("❌ GITHUB_TOKEN not found in .env file")
    exit(1)

print(f"✅ GitHub token loaded: {github_token[:10]}...")

# Possible Claude model names to test
claude_models = [
    "claude-3-5-sonnet",
    "claude-3.5-sonnet",
    "claude-sonnet-3.5",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-latest",
    "anthropic.claude-3-5-sonnet",
    "Anthropic.Claude-3.5-Sonnet",
    "claude-3.5-sonnet",
    "claude-3.5-sonnet-v2",
    "claude-sonnet-4.5",  # User mentioned "Claude Sonnet 4.5"
    "claude-4.5-sonnet",
]

endpoint = "https://models.inference.ai.azure.com/chat/completions"

print("\n" + "="*70)
print("Testing Claude Model Names")
print("="*70 + "\n")

for model_name in claude_models:
    print(f"Testing: {model_name}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    }
    
    data = {
        "messages": [
            {"role": "user", "content": "Say 'hi'"}
        ],
        "model": model_name,
        "temperature": 0.7,
        "max_tokens": 10
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS: {model_name} is available!")
            result = response.json()
            print(f"   Response: {result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')}")
            print()
        elif response.status_code == 400:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
            if "Unknown model" in error_message:
                print(f"   ❌ NOT AVAILABLE: {model_name}")
            else:
                print(f"   ⚠️  ERROR: {error_message}")
        elif response.status_code == 401:
            print(f"   ❌ AUTH ERROR: GitHub token is invalid or expired")
            print("   Please update your token and try again")
            break
        else:
            print(f"   ⚠️  HTTP {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"   ⚠️  EXCEPTION: {str(e)}")
    
    print()

print("="*70)
print("\n💡 To find all available models, visit:")
print("   https://github.com/marketplace/models")
print("\n   Or check the GitHub Models documentation")
