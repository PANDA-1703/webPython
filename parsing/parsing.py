from bs4 import BeautifulSoup
import mysql.connector


# Читаем файл html
with open("site.html", "r", encoding="utf-8") as file:
    html_code = file.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_code, "html.parser")

# Находим все таблицы с классом "wikitable"
tables = soup.find_all("table", class_="wikitable")

# Подключение к базе данных MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="weapons"
)

# Создание курсора для выполнения SQL-запросов
cursor = connection.cursor()

# SQL-запрос для создания таблицы, если она не существует
create_table_query = """
CREATE TABLE IF NOT EXISTS weapons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  weapon_name VARCHAR(255),
  caliber VARCHAR(500),
  in_service VARCHAR(500),
  variants VARCHAR(1000),
  country VARCHAR(255),
  wiki_link VARCHAR(500),
  ruxpert_link VARCHAR(500),
  weaponland_link VARCHAR(500)
)
"""

# Выполнение SQL-запроса для создания таблицы
cursor.execute(create_table_query)

# Проходимся по каждой таблице
for table in tables:
    # Находим все строки в таблице
    rows = table.find_all("tr")

    # Проходимся по каждой строке и извлекаем данные
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 6:
            weapon_name = columns[0].text.strip()
            caliber = columns[1].text.strip()
            in_service = columns[2].text.strip()
            variants = columns[3].text.strip()
            country = columns[5].text.strip()

            # Создаем ссылку на википедию для оружия
            wiki_link = f"https://ru.wikipedia.org/wiki/{weapon_name.replace(' ', '_')}"
            ruxpert_link = f"https://ruxpert.ru/Российское_пехотное_оружие#{weapon_name.replace(' ', '_')}"
            weaponland_link = f"https://weaponland.ru/"

            # SQL-запрос для вставки данных в таблицу
            query = "INSERT INTO weapons (weapon_name, caliber, in_service, variants, country, wiki_link, ruxpert_link, weaponland_link)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (weapon_name, caliber, in_service, variants, country, wiki_link, ruxpert_link, weaponland_link)

            # Выполнение SQL-запроса
            cursor.execute(query, values)

            # Фиксация изменений в базе данных
            connection.commit()

          