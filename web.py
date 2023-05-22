from flask import Flask, render_template, request, flash
from wtforms import Form, StringField, validators
import mysql.connector

app = Flask(__name__)

# Подключение к базе данных MySQL
connection = mysql.connector.connect(
    host="dist/weapons.ibd",
    user="root",
    password="0000",
    database="weapons"
)

# Класс формы для ввода названия оружия
class WeaponSearchForm(Form):
    weapon_name = StringField('Weapon Name', [validators.DataRequired()])

# Маршрут для главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    form = WeaponSearchForm(request.form)

    if request.method == 'POST' and form.validate():
        weapon_name = form.weapon_name.data

        cursor = connection.cursor()

        query = "SELECT * FROM weapons WHERE weapon_name LIKE %s"
        values = (f'%{weapon_name}%',)

        cursor.execute(query, values)
        result = cursor.fetchone()

        cursor.fetchall()  # Строка, чтобы прочитать остаток результатов

        cursor.close()

        if result:
            weapon_info = {
                'weapon_name': result[1],
                'caliber': result[2],
                'in_service': result[3],
                'variants': result[4],
                'country': result[5],
                'wiki_link': result[6],
                'ruxpert_link': result[7],
                'weaponland_link': result[8]
            }
            submitted = True
        else:
            weapon_info = None
            flash('Оружие не найдено.', 'danger')
            submitted = True
    else:
        weapon_info = None
        submitted = False

    return render_template('index.html', form=form, weapon_info=weapon_info, submitted=submitted)


if __name__ == '__main__':
    app.run()
