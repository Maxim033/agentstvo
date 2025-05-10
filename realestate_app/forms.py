from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed
from realestate_app.config_site import ConfigSite

class PropertyForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Описание')
    price = IntegerField('Цена', validators=[DataRequired(), NumberRange(min=1)])
    address = StringField('Адрес', validators=[DataRequired(), Length(max=200)])
    rooms = IntegerField('Комнаты', validators=[NumberRange(min=1)])
    area = FloatField('Площадь (м²)', validators=[NumberRange(min=1)])
    property_type = SelectField('Тип', choices=[
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('commercial', 'Коммерческая')
    ])
    image = FileField('Изображение', validators=[
        FileAllowed(ConfigSite.ALLOWED_EXTENSIONS, 'Только изображения!')
    ])
    submit = SubmitField('Сохранить')

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')