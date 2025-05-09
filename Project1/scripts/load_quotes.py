import sys
import os

# Додаємо шлях до каталогу, де знаходиться `models`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))

# Тепер імпортуємо моделі
from models import Author, Quote


