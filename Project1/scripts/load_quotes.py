import json
from models.models import Author, Quote

with open('data/quotes.json', 'r', encoding='utf-8') as f:
    quotes = json.load(f)

for item in quotes:
    author = Author.objects(fullname=item['author']).first()
    if author:
        quote = Quote(tags=item['tags'], author=author, quote=item['quote'])
        quote.save()
