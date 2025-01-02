from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location', validators=[DataRequired(), URL(message="Please enter a valid URL")])
    open_time = StringField('Open time', validators=[DataRequired()])
    close_time = StringField('Close time', validators=[DataRequired()])
    wifi_rate = SelectField('Wi-Fi Rate', choices=[
        ('1', '💪'),
        ('2', '💪💪'),
        ('3', '💪💪💪'),
        ('4', '💪💪💪💪'),
        ('5', '💪💪💪💪💪'),
        ('6', '✘')
    ])
    coffee_rate = SelectField('Coffee Rate', choices=[
        ('1', '☕️'),
        ('2', '☕️☕️'),
        ('3', '☕️☕️☕️'),
        ('4', '☕️☕️☕️☕️'),
        ('5', '☕️☕️☕️☕️☕️')
    ])
    power_rate = SelectField('Power Rate', choices=[
        ('1', '🔌'),
        ('2', '🔌🔌'),
        ('3', '🔌🔌🔌'),
        ('4', '🔌🔌🔌🔌'),
        ('5', '🔌🔌🔌🔌🔌')
    ])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                form.cafe.data,
                form.location_url.data,
                form.open_time.data,
                form.close_time.data,
                form.coffee_rate.data,
                form.wifi_rate.data,
                form.power_rate.data,
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    try:
        with open('cafe-data.csv', encoding="UTF-8", newline='') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = list(csv_data)
            if not list_of_rows:
                raise ValueError("CSV file is empty.")
            headers = list_of_rows[0]
        return render_template('cafes.html', cafes=list_of_rows, headers=headers)
    except (FileNotFoundError, ValueError) as e:
        return render_template('cafes.html', cafes=[], headers=[], error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
