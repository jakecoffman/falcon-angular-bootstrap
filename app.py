import falcon
from views import UsersResource

app = falcon.API()

users_resource = UsersResource()

app.add_route("/users", users_resource)
app.add_route("/users/{user_id}", users_resource)

# For debugging. A performant way to launch is gunicorn.
if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8080, app)
    httpd.serve_forever()
