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
    __tablename__= 'concept'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    group = db.Column(db.String(128))

    pages = db.relationship('ConceptPages',back_populates='concept')
    words =db.relationship('Word', backref='concept', lazy='dynamic')

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return '<Concept %r>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ConceptPages(db.Model):
    __tablename__= 'concept_pages'
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'),primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'),primary_key=True)
    degree = db.Column(db.Float(64))
    pagerank = db.Column(db.Float(64))
    camino = db.Column(db.String(64))
    frequency = db.Column(db.Integer)
    concept = db.relationship("Concept", back_populates="pages")
    page = db.relationship("Page", back_populates="concepts")


'''
concept_pages = db.Table('concept_pages',
                         db.Column('concept_id', db.Integer, db.ForeignKey('concept.id')),
                         db.Column('page_id', db.Integer, db.ForeignKey('page.id')),
                         db.Column('degree ', db.Float),
                        db.Column('pagerank ', db.Float),
                        db.Column('camino ', db.Boolean),
                         db.Column('frequency ', db.Float))'''

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer)
    target_id= db.Column(db.Integer)

    def __init__(self, source_id,target_id):
        self.source_id = source_id
        self.target_id = target_id


class Page(db.Model):
    __tablename__= 'page'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(128))
    path = db.Column(db.String(128))
    concepts = db.relationship('ConceptPages',back_populates='page')


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





