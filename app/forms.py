from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ScheduleFilterForm(FlaskForm):
    group_name = StringField('Название группы')
    teacher_name = StringField('Имя преподавателя')
    submit = SubmitField('Найти расписание')