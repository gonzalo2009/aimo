from peewee import *

db = SqliteDatabase('notes.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Note(BaseModel):
    user = ForeignKeyField(User, backref='notes')
    message = TextField()


   
