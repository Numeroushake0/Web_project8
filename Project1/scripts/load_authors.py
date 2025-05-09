import json
from models.models import Author

with open('data/authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)

for item in authors:
    author = Author(**item)
    author.save()

