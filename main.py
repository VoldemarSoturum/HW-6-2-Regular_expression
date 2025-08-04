from pprint import pprint
import csv
import re

# Чтение исходного файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Задание 1: Приведение ФИО к стандартному формату
for contact in contacts_list[1:]:
    # Объединение первых трех полей и разбиение по пробелам
    full_name = ' '.join(contact[:3]).split()
    # Распределение значений в зависимости от их количества
    if len(full_name) == 3:
        contact[0], contact[1], contact[2] = full_name
    elif len(full_name) == 2:
        contact[0], contact[1] = full_name
        contact[2] = ''
    elif len(full_name) == 1:
        contact[0] = full_name[0]
        contact[1], contact[2] = '', ''

# Задание 2: Нормализация телефонных номеров
phone_pattern = re.compile(
    r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
    r'(\s*\(?(доб\.?)\s*(\d+)\)?)?'
) # Регулярное выражение для поиска номеров телефонов

for contact in contacts_list[1:]:
    phone = contact[5] # Индекс 5 соответствует номеру телефона
    # Проверка наличия номера телефона
    if phone:
        match = phone_pattern.search(phone) # Поиск совпадений с шаблоном
        # Если номер соответствует шаблону
        if match:
            # Форматирование основного номера
            formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
            # Добавление доб. номера при наличии
            if match.group(7) and match.group(8):
                formatted_phone += f" доб.{match.group(8)}"
            contact[5] = formatted_phone

# Задание 3: Объединение дублирующихся записей
contacts_dict = {} # Словарь для хранения уникальных контактов
# Используем ключ (Фамилия, Имя) для идентификации дубликатов
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])  # Ключ: Фамилия + Имя
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        # Объединение информации из дублирующих записей
        for i in range(len(contact)):
            if contact[i] and not contacts_dict[key][i]:
                contacts_dict[key][i] = contact[i]

# Формирование итогового списка
unique_contacts = [contacts_list[0]] + list(contacts_dict.values())

# Сохранение результата в новый CSV файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(unique_contacts)

# Вывод результата для проверки
pprint(unique_contacts)