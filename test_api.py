#!/usr/bin/env python
"""Test API configuration and ChatGPT client"""

from config import Config
from api.chatgpt_client import ChatGPTClient

print("=" * 50)
print("API Configuration Test")
print("=" * 50)
print(f"API Key present: {bool(Config.OPENAI_API_KEY)}")
if Config.OPENAI_API_KEY:
    key = Config.OPENAI_API_KEY
    print(f"API Key preview: {key[:30]}...")
    print(f"API Key length: {len(key)}")

print("\nTesting ChatGPT Client...")
client = ChatGPTClient()
print(f"Client initialized: {client is not None}")
print(f"OpenAI client ready: {client.is_real}")

print("\nTesting API call...")
result = client.analyze_side_effects("aspirin")
print(f"Result (first 100 chars): {result[:100] if result else 'None'}")
print(f"\nFull result:\n{result}")
