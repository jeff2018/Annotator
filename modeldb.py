from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


app = Flask(__name__)
app.config['SECRET_KEY'] = '5d3bae549ae7c89b2d1be949'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


pdf_concepts = db.Table('pdf_concepts',
                        db.Column('pdf_id', db.Integer, db.ForeignKey('pdf_document.id')),
                        db.Column('concept_id', db.Integer, db.ForeignKey('concept.id')))

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

class PDFDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    path = db.Column(db.String(256))
    pages = db.relationship('Page',backref='pdfdocument',lazy='dynamic')
    concepts = db.relationship('Concept', secondary=pdf_concepts,
                               backref=db.backref('pdfdocuments', lazy='dynamic'))

    def __init__(self, name, path, pages=[], annotations=[]):
        self.name = name
        self.path = path
        self.pages = pages
        self.annotations = annotations

    def __repr__(self):
        return '<PDF %r>' % self.name

class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    words =db.relationship('Word', backref='concept', lazy='dynamic')

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return '<Concept %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

concept_pages = db.Table('concept_pages',
                         db.Column('concept_id', db.Integer, db.ForeignKey('concept.id')),
                         db.Column('page_id', db.Integer, db.ForeignKey('page.id')))

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(128))
    path = db.Column(db.String(128))
    concepts = db.relationship('Concept', secondary=concept_pages,
                                backref=db.backref('pages', lazy='dynamic'))


    id_pdf = db.Column(db.Integer, db.ForeignKey('pdf_document.id'))

    def __init__(self, number,path):
        self.number = number
        self.path = path


    def __repr__(self):
        return '<Page %r>' % self.number

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    id_concept = db.Column(db.Integer, db.ForeignKey('concept.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Concept %r>' % self.name





