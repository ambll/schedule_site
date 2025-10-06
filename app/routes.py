from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Lesson, Group, Teacher, Discipline, Classroom, LessonType
from app.forms import LessonForm, GroupForm, TeacherForm, DisciplineForm
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

def get_form_choices():
    """Получение данных для выпадающих списков"""
    return {
        'disciplines': [(d.id, d.name) for d in Discipline.query.filter_by(is_active=True).all()],
        'groups': [(g.id, g.name) for g in Group.query.filter_by(is_active=True).all()],
        'teachers': [(t.id, t.fullname) for t in Teacher.query.filter_by(is_active=True).all()],
        'classrooms': [(c.id, c.number) for c in Classroom.query.all()],
        'lesson_types': [(lt.id, lt.name) for lt in LessonType.query.all()]
    }

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/schedule')
def schedule():
    group_name = request.args.get('group_name', '').strip()
    teacher_name = request.args.get('teacher_name', '').strip()
    
    query = db.session.query(Lesson).\
        join(Group, Lesson.group_id == Group.id).\
        join(Teacher, Lesson.teacher_id == Teacher.id).\
        join(Discipline, Lesson.discipline_id == Discipline.id).\
        join(Classroom, Lesson.classroom_id == Classroom.id).\
        join(LessonType, Lesson.lesson_type_id == LessonType.id)
    
    if group_name:
        query = query.filter(Group.name.ilike(f'%{group_name}%'))
    
    if teacher_name:
        query = query.filter(Teacher.fullname.ilike(f'%{teacher_name}%'))
    
    lessons = query.order_by(Lesson.date, Lesson.lesson_num).all()
    
    all_groups = Group.query.filter_by(is_active=True).order_by(Group.name).all()
    all_teachers = Teacher.query.filter_by(is_active=True).order_by(Teacher.fullname).all()
    
    return render_template('schedule.html',
                         lessons=lessons,
                         group_name=group_name,
                         teacher_name=teacher_name,
                         all_groups=all_groups,
                         all_teachers=all_teachers)

# Маршруты для добавления данных
@bp.route('/add/lesson', methods=['GET', 'POST'])
def add_lesson():
    form = LessonForm()
    choices = get_form_choices()
    
    # Заполняем выпадающие списки
    form.discipline_id.choices = choices['disciplines']
    form.group_id.choices = choices['groups']
    form.teacher_id.choices = choices['teachers']
    form.classroom_id.choices = choices['classrooms']
    form.lesson_type_id.choices = choices['lesson_types']
    
    if form.validate_on_submit():
        try:
            lesson = Lesson(
                discipline_id=form.discipline_id.data,
                group_id=form.group_id.data,
                teacher_id=form.teacher_id.data,
                classroom_id=form.classroom_id.data,
                date=form.date.data,
                lesson_num=form.lesson_num.data,
                lesson_type_id=form.lesson_type_id.data
            )
            db.session.add(lesson)
            db.session.commit()
            flash('Занятие успешно добавлено!', 'success')
            return redirect(url_for('main.schedule'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении занятия: {str(e)}', 'danger')
    
    return render_template('add_lesson.html', form=form, title='Добавить занятие')

@bp.route('/add/group', methods=['GET', 'POST'])
def add_group():
    form = GroupForm()
    
    if form.validate_on_submit():
        try:
            group = Group(
                name=form.name.data,
                is_active=form.is_active.data
            )
            db.session.add(group)
            db.session.commit()
            flash('Группа успешно добавлена!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении группы: {str(e)}', 'danger')
    
    return render_template('add_form.html', form=form, title='Добавить группу')

@bp.route('/add/teacher', methods=['GET', 'POST'])
def add_teacher():
    form = TeacherForm()
    
    if form.validate_on_submit():
        try:
            teacher = Teacher(
                fullname=form.fullname.data,
                mtslink=form.mtslink.data,
                is_active=form.is_active.data
            )
            db.session.add(teacher)
            db.session.commit()
            flash('Преподаватель успешно добавлен!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении преподавателя: {str(e)}', 'danger')
    
    return render_template('add_teacher.html', form=form, title='Добавить преподавателя')

@bp.route('/add/discipline', methods=['GET', 'POST'])
def add_discipline():
    form = DisciplineForm()
    
    if form.validate_on_submit():
        try:
            discipline = Discipline(
                name=form.name.data,
                is_active=form.is_active.data
            )
            db.session.add(discipline)
            db.session.commit()
            flash('Дисциплина успешно добавлена!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении дисциплины: {str(e)}', 'danger')
    
    return render_template('add_form.html', form=form, title='Добавить дисциплину')

# Старые маршруты для просмотра таблиц
@bp.route('/tables')
def tables():
    result = db.session.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'schedule'
        ORDER BY table_name;
    """))
    tables = [row[0] for row in result]
    return render_template('tables.html', tables=tables)

@bp.route('/table/<table_name>')
def show_table(table_name):
    result = db.session.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'schedule' AND table_name = :table_name;
    """), {'table_name': table_name})
    
    if result.fetchone() is None:
        return "Table not found", 404
    
    data = db.session.execute(text(f'SELECT * FROM schedule."{table_name}"')).fetchall()
    
    columns_result = db.session.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'schedule' AND table_name = :table_name;
    """), {'table_name': table_name})
    
    columns = [row[0] for row in columns_result]
    
    return render_template('table.html', 
                           table_name=table_name, 
                           columns=columns, 
                           data=data)