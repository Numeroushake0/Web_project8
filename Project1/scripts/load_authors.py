import json
from models import Author, Quote

with open('data/authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)

for item in authors:
    author = Author(**item)
    author.save()

