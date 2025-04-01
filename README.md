# ✈️ AirportFlightManager

Уеб-базирана система за **следене и управление на полетите в летище**, разработена с **Django REST Framework**. Поддържа търсене на полети от пътници и справки за предстоящи полети от членове на екипажа.

---

## 📌 Основни функционалности

### ✅ За пътници
- Търсене на полети по дестинация, номер, интервал от часове
- Преглед на детайли за полети

### 🤝‍✈️ За членове на екипажа
- Справка за предстоящи полети
- Преглед на съекипници и роли

### 🛠️ За оператори/администратори
- CRUD операции над полети
- Добавяне и редакция на летища, авиокомпании, екипажи, апарати
- Управление на роли: Admin, Inspector, CrewMember, Observer

---

## ⚙️ Технологии

- Python 3.11+
- Django 5.1
- Django REST Framework
- SQLite (development)
- JWT (production-ready)
- Docker (optional)

---

## 🚀 Стартиране на проекта

```bash
git clone https://github.com/omer-mestan/AIRPORT_MANAGER.git
cd AIRPORT_MANAGER
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🗂️ API крайни точки

| Method | URL                          | Описание                                 | Достъп |
|--------|------------------------------|------------------------------------------|--------|
| GET    | `/api/flights/`             | Списък от полети с филтриране            | Всички |
| GET    | `/api/flights/?destination=London` | Търсене по дестинация            | Всички |
| GET    | `/api/my-crew-flights/`     | Предстоящи полети за екипаж              | Само CrewMember |
| PATCH  | `/api/flights/<id>/`        | Редакция на полет                        | Admin, Inspector |

---

## 👥 Роли и Права

- **Admin**: Пълен достъп
- **Inspector**: CRUD над полети
- **CrewMember**: Само своите полети
- **Passenger**: Търсене и преглед

Правата са имплементирани чрез custom permissions: `IsAdminOrInspectorForWrite`, `IsCrewUser`.

---

## ✅ Тестване

```bash
python manage.py test
```

- Тестови модули: `django.test`, `rest_framework.test`
- Покрития: търсене, достъп, ограничения, полезни сценарии

---

## 👨‍💼 Автори

- Юмер Местан – [omer987@outlook.com](mailto:omer987@outlook.com)
- Христо Стоилов
- Алекс Тенев
- Димитър Георгиев

Проект към Ту-София – Факултет по ИТИ

---

## 📄 Лиценз

# LICENSE

© 2025 Юмер Местан и екипът на AIRPORT_MANAGER

Този проект е лицензиран под Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

✅ Разрешено е използването, споделянето и модифицирането на проекта **само за некомерсиални цели**, при условие че авторите са упоменати.

❌ Не се разрешава използване за търговски цели без писмено разрешение.

📄 Пълният лиценз е достъпен на:  
https://creativecommons.org/licenses/by-nc/4.0/legalcode

Софтуерът е с образователска цел. Всички права запазени от авторите.
