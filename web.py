from flask import Flask, render_template, request, flash
from wtforms import Form, StringField, validators
import csv

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Чтение данных из CSV-файла
csv_file = "weapons.csv"
weapons_data = []

with open(csv_file, "r", newline="") as file:
    reader = csv.reader(file)
    headers = next(reader)  # Пропустить заголовки
    for row in reader:
        weapons_data.append(dict(zip(headers, row)))

# Класс формы для ввода названия оружия
class WeaponSearchForm(Form):
    weapon_name = StringField('Weapon Name', [validators.DataRequired()])

# Маршрут для главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    form = WeaponSearchForm(request.form)

    if request.method == 'POST' and form.validate():
        weapon_name = form.weapon_name.data

        weapon_info = None
        submitted = False

        for weapon in weapons_data:
            if weapon['weapon_name'].lower().find(weapon_name.lower()) != -1:
                weapon_info = {
                    'weapon_name': weapon['weapon_name'],
                    'caliber': weapon['caliber'],
                    'in_service': weapon['in_service'],
                    'variants': weapon['variants'],
                    'country': weapon['country'],
                    'wiki_link': weapon['wiki_link'],
                    'ruxpert_link': weapon['ruxpert_link'],
                    'weaponland_link': weapon['weaponland_link']
                }
                submitted = True
                break

        if not weapon_info:
            flash('Оружие не найдено.', 'danger')
            submitted = True

        return render_template('index.html', form=form, weapon_info=weapon_info, submitted=submitted)

    return render_template('index.html', form=form, weapon_info=None, submitted=False)

if __name__ == '__main__':
    app.run()
