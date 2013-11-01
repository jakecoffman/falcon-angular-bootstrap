import json
import falcon
import peewee


db = peewee.SqliteDatabase('users.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField()
    email = peewee.CharField()

    def __str__(self):
        return json.dumps({
            'username': self.username,
            'email': self.email
        })


class UsersResource(object):
    def on_get(self, request, response, user_id=None):
        if user_id is None:
            response.body = json.dumps([u.username for u in User.select()])
        else:
            user = User.get(username=user_id)
            response.body = str(user)


app = falcon.API()

users_resource = UsersResource()

app.add_route("/users", users_resource)
app.add_route("/users/{user_id}", users_resource)

# For debugging. A performant way to launch is gunicorn.
if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8080, app)
    httpd.serve_forever()
