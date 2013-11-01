import json
import falcon
import peewee


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


class UsersResource(object):
    def on_get(self, request, response, user_id=None):
        if user_id is None:
            response.body = json.dumps([u.username for u in User.select()])
        else:
            user = User.get(username=user_id)
            response.body = str(user)

    def on_post(self, request, response):
        raw = request.stream.read()  # read fail?
        data = json.loads(raw)  # json fail?
        if 'username' not in data or 'email' not in data:
            raise falcon.HTTPError(falcon.HTTP_400, "Invalid JSON", "Please send a hash with 'username' and 'email'")
        user = User.create(username=data['username'], email=data['email'])
        user.save()
        response.status = falcon.HTTP_201
        response.location = '/users/%s' % user.username

    def on_delete(self, request, response, user_id):
        user = User.get(username=user_id)
        user.delete_instance()
        response.location = '/users'

    def on_put(self, request, response, user_id):
        raw = request.stream.read()
        data = json.loads(raw)
        if 'email' not in data:
            raise falcon.HTTPError(falcon.HTTP_400, "Invalid JSON", "Please send a hash with 'email'")
        user = User.get(username=user_id)
        user.email = data['email']
        user.save()
        response.location = '/users/%s' % user.username


app = falcon.API()

users_resource = UsersResource()

app.add_route("/users", users_resource)
app.add_route("/users/{user_id}", users_resource)

# For debugging. A performant way to launch is gunicorn.
if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8080, app)
    httpd.serve_forever()
