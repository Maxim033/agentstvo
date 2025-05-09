from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PropertyForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = IntegerField('Цена', validators=[DataRequired(), NumberRange(min=1)])
    address = StringField('Адрес', validators=[DataRequired()])
    rooms = IntegerField('Количество комнат', validators=[NumberRange(min=1)])
    area = FloatField('Площадь (м²)', validators=[NumberRange(min=1)])
    property_type = SelectField('Тип недвижимости', choices=[
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('commercial', 'Коммерческая')
    ])
    submit = SubmitField('Сохранить')