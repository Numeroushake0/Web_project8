import os
import json
import re
from mongoengine import connect
from dotenv import load_dotenv
from redis import Redis
from models import Author, Quote


# Завантаження .env
load_dotenv()

# Підключення до MongoDB
connect(host=os.getenv("MONGODB_URI"))

# Підключення до Redis
redis_client = Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)

# ---- Функції ----

def cache_or_query(cache_key, query_func):
    """Повертає кешований результат або виконує запит і кешує результат"""
    if redis_client.exists(cache_key):
        print(f"[CACHE] Результат з кешу: {cache_key}")
        return json.loads(redis_client.get(cache_key))
    else:
        result = query_func()
        redis_client.set(cache_key, json.dumps(result, ensure_ascii=False), ex=3600)  # кеш на 1 годину
        return result

def find_by_author(name):
    regex = re.compile(f'^{name}', re.IGNORECASE)
    author = Author.objects(fullname=regex).first()
    if not author:
        return [f"Автор '{name}' не знайдений."]
    
    def query():
        return [q.quote for q in Quote.objects(author=author)]
    
    return cache_or_query(f"name:{name}", query)

def find_by_tag(tag):
    regex = re.compile(f'^{tag}', re.IGNORECASE)

    def query():
        return [q.quote for q in Quote.objects(tags__iregex=regex.pattern)]
    
    return cache_or_query(f"tag:{tag}", query)

def find_by_tags(tag_list):
    def query():
        return [q.quote for q in Quote.objects(tags__in=tag_list)]
    return query()

# ---- Головний цикл ----

def main():
    print("📚 Введіть команду (name:NAME, tag:TAG, tags:TAG1,TAG2,... або exit):")
    while True:
        command = input(">>> ").strip()
        if command == "exit":
            print("👋 Вихід.")
            break

        if command.startswith("name:"):
            name = command.split(":", 1)[1].strip()
            results = find_by_author(name)
        elif command.startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            results = find_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].split(",")
            tags = [t.strip() for t in tags]
            results = find_by_tags(tags)
        else:
            print("⚠️ Невідома команда.")
            continue

        print("\n".join(results) if results else "Нічого не знайдено.")

if __name__ == "__main__":
    main()
