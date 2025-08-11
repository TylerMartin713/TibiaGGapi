#!/usr/bin/env python
import requests

# Test the TibiaData API directly
print("Testing TibiaData API...")
response = requests.get("https://api.tibiadata.com/v4/creature/Dragon")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    creature_data = data.get("creature", {})
    print(f"Name: {creature_data.get('name', '')}")
    print(f"Image URL: {creature_data.get('image_url', '')}")
    print(f"HP: {creature_data.get('hitpoints', 0)}")
    print(f"XP: {creature_data.get('experience_points', 0)}")
else:
    print(f"Error: {response.text}")
