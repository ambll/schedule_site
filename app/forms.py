from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class LessonForm(FlaskForm):
    discipline_id = SelectField('Дисциплина', coerce=int, validators=[DataRequired()])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Преподаватель', coerce=int, validators=[DataRequired()])
    classroom_id = SelectField('Аудитория', coerce=int, validators=[DataRequired()])
    date = DateField('Дата', validators=[DataRequired()])
    lesson_num = IntegerField('Номер урока', validators=[DataRequired()])
    lesson_type_id = SelectField('Тип занятия', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить занятие')

class GroupForm(FlaskForm):
    name = StringField('Название группы', validators=[DataRequired()])
    is_active = BooleanField('Активная', default=True)
    submit = SubmitField('Добавить группу')

class TeacherForm(FlaskForm):
    fullname = StringField('ФИО преподавателя', validators=[DataRequired()])
    photo = FileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    mtslink = StringField('Ссылка MTS')
    is_active = BooleanField('Активный', default=True)
    submit = SubmitField('Добавить преподавателя')

class DisciplineForm(FlaskForm):
    name = StringField('Название дисциплины', validators=[DataRequired()])
    is_active = BooleanField('Активная', default=True)
    submit = SubmitField('Добавить дисциплину')