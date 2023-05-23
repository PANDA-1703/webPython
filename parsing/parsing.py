from bs4 import BeautifulSoup
import csv

# Читаем файл html
with open("parsing/site.html", "r", encoding="utf-8") as file:
    html_code = file.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_code, "html.parser")

# Находим все таблицы с классом "wikitable"
tables = soup.find_all("table", class_="wikitable")

# Открываем файл CSV для записи
with open("weapons.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    headers = ["weapon_name", "caliber", "in_service", "variants", "country", "wiki_link", "ruxpert_link", "weaponland_link"]
    writer.writerow(headers)

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

                # Создаем ссылки на сайты с оружием
                wiki_link = f"https://ru.wikipedia.org/wiki/{weapon_name.replace(' ', '_')}"
                ruxpert_link = f"https://ruxpert.ru/Российское_пехотное_оружие#{weapon_name.replace(' ', '_')}"
                weaponland_link = f"https://weaponland.ru/"

                # Записываем данные в CSV файл
                writer.writerow([weapon_name, caliber, in_service, variants, country, wiki_link, ruxpert_link, weaponland_link])
