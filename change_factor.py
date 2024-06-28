import pandas as pd
from transliterate import translit

# Загрузка данных с указанием правильного разделителя и кодировки
df = pd.read_csv('Y:/444.csv', encoding='windows-1251', delimiter=';')

# Функция для создания нового username
def create_username(row):
    lastname = translit(row['lastname'], 'ru', reversed=True)
    firstname = translit(row['firstname'], 'ru', reversed=True)
    fathername = translit(row['fathername'], 'ru', reversed=True)
    return f"{lastname}-{firstname}-{fathername}-@mail.ru".lower()

# Применение функции к каждой строке
df['email'] = df.apply(create_username, axis=1)

# Сохранение обновлённого файла
df.to_csv('555.csv', index=False, encoding='windows-1251', sep=';')