import peewee
import json

db = peewee.SqliteDatabase('users.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(primary_key=True)
    email = peewee.CharField()

    def __str__(self):
        return json.dumps({
            'username': self.username,
            'email': self.email
        })
