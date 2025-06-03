# 🗂️ Projekt ogłoszeniowy – Django REST + GraphQL

Projekt backendowy zrealizowany w ramach przedmiotu **Zaawansowane Aplikacje Internetowe**  
(studia stacjonarne, semestr letni 2024/2025)

---

## 📦 Opis

System ogłoszeniowy z obsługą użytkowników, moderacji i wgrywania obrazów.  
Umożliwia zarządzanie ogłoszeniami, kategoriami, tagami i ulubionymi ofertami.

Projekt oparty na:
- Django 5.x
- Django REST Framework (DRF)
- Graphene-Django (GraphQL)
- JWT (SimpleJWT)
- Obsługa plików `media/` i generowania miniatur
- Testy jednostkowe (REST, GraphQL, media, uprawnienia)

---

## 🚀 Uruchamianie lokalne

```bash
git clone <repo>
cd ZAI_Projekt
python -m venv .venv
source .venv/bin/activate  # lub .venv\Scripts\activate na Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
