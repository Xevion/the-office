"""
data.py

Manages API quote/character data, caching static responses and reloading from disk.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data', 'data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(os.path.join(BASE_DIR, 'data', 'characters.json'), 'r', encoding='utf-8') as file:
    character_data = json.load(file)

