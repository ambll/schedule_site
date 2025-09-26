from app import db

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    number = db.Column(db.String(30), nullable=False)

class Discipline(db.Model):
    __tablename__ = 'disciplines'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

class LessonType(db.Model):
    __tablename__ = 'lesson_types'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255))
    mtslink = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False)

class Lesson(db.Model):
    __tablename__ = 'lessons'
    __table_args__ = {'schema': 'schedule'}
    
    id = db.Column(db.BigInteger, primary_key=True)
    discipline_id = db.Column(db.BigInteger, db.ForeignKey('schedule.disciplines.id'))
    group_id = db.Column(db.BigInteger, db.ForeignKey('schedule.groups.id'))
    teacher_id = db.Column(db.BigInteger, db.ForeignKey('schedule.teachers.id'))
    classroom_id = db.Column(db.BigInteger, db.ForeignKey('schedule.classrooms.id'))
    date = db.Column(db.Date)
    lesson_num = db.Column(db.SmallInteger, nullable=False)
    lesson_type_id = db.Column(db.BigInteger, db.ForeignKey('schedule.lesson_types.id'))
    
    # Связи
    discipline = db.relationship('Discipline', backref='lessons')
    group = db.relationship('Group', backref='lessons')
    teacher = db.relationship('Teacher', backref='lessons')
    classroom = db.relationship('Classroom', backref='lessons')
    lesson_type = db.relationship('LessonType', backref='lessons')