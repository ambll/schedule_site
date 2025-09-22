from flask import Blueprint, render_template
from app import db
from sqlalchemy import text

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Получаем список всех таблиц в схеме 'schedule'
    result = db.session.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'schedule'
        ORDER BY table_name;
    """))
    tables = [row[0] for row in result]
    return render_template('index.html', tables=tables)

@bp.route('/table/<table_name>')
def show_table(table_name):
    # Важно: Проверяем, что table_name есть в списке таблиц, чтобы избежать SQL-инъекций
    result = db.session.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'schedule' AND table_name = :table_name;
    """), {'table_name': table_name})
    
    if result.fetchone() is None:
        return "Table not found", 404
    
    # Получаем данные из таблицы
    data = db.session.execute(text(f'SELECT * FROM schedule."{table_name}"')).fetchall()  # И здесь тоже
    
    # Получаем названия столбцов
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