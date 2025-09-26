from flask import Blueprint, render_template, request
from app import db
from app.models import Lesson, Group, Teacher, Discipline, Classroom, LessonType
from sqlalchemy import text, or_

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/schedule')
def schedule():
    group_name = request.args.get('group_name', '').strip()
    teacher_name = request.args.get('teacher_name', '').strip()
    
    # Базовый запрос с JOIN всех связанных таблиц
    query = db.session.query(Lesson).\
        join(Group, Lesson.group_id == Group.id).\
        join(Teacher, Lesson.teacher_id == Teacher.id).\
        join(Discipline, Lesson.discipline_id == Discipline.id).\
        join(Classroom, Lesson.classroom_id == Classroom.id).\
        join(LessonType, Lesson.lesson_type_id == LessonType.id)
    
    # Применяем фильтры
    if group_name:
        query = query.filter(Group.name.ilike(f'%{group_name}%'))
    
    if teacher_name:
        query = query.filter(Teacher.fullname.ilike(f'%{teacher_name}%'))
    
    # Сортируем по дате и номеру урока
    lessons = query.order_by(Lesson.date, Lesson.lesson_num).all()
    
    # Получаем списки всех групп и преподавателей для автодополнения
    all_groups = Group.query.filter_by(is_active=True).order_by(Group.name).all()
    all_teachers = Teacher.query.filter_by(is_active=True).order_by(Teacher.fullname).all()
    
    return render_template('schedule.html',
                         lessons=lessons,
                         group_name=group_name,
                         teacher_name=teacher_name,
                         all_groups=all_groups,
                         all_teachers=all_teachers)

@bp.route('/tables')
def tables():
    # Старая функциональность просмотра таблиц (оставляем на всякий случай)
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