import os
import bcrypt
from peewee import *
from datetime import datetime

# Настройка базы данных
db = SqliteDatabase('todo.db')

class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = AutoField()
    name = CharField(unique=True, max_length=50)
    description = CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True, max_length=64)
    email = CharField(unique=True, max_length=120, null=True)
    password_hash = CharField(max_length=128)
    role = ForeignKeyField(Role, backref='users')
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __str__(self):
        return self.username

class Todo(BaseModel):
    id = AutoField()
    title = CharField(max_length=100)
    description = TextField(null=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField(null=True)

    def __str__(self):
        return self.title

class Options(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    description = TextField(null=True)
    user_id = IntegerField(null=True)  # None for global options
    category = CharField(max_length=50, null=True)
    value = TextField(null=True)

    def __str__(self):
        return self.name

# Создание таблиц
def create_tables():
    with db:
        db.create_tables([Role, User, Todo, Options])

# Инициализация базы данных
if __name__ == '__main__':
    create_tables()