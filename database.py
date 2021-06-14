from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Point(db.Model):
    __tablename__ = "points"
    id = db.Column(db.Integer, primary_key=True)
    point_name = db.Column('pointName', db.String(15))
    latitude = db.Column('Latitude', db.Float)
    longitude = db.Column('Longitude', db.Float)
    address = db.Column('Address', db.Unicode(255))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'links'
    link_name = db.Column('linkName', db.String(15))
    distance = db.Column('distance', db.Float)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(36), unique=True)
    status = db.Column('status', db.String(7), default='running')
    points = db.relationship(Point, backref='task')
    links = db.relationship(Link, backref='task')
