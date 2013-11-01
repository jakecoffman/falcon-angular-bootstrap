import json
import falcon

class JSONResource(object):
    def on_get(self, request, response):
        json_data = {"message": "Hello, world!"}
        response.body = json.dumps(json_data)

app = falcon.API()

json_resource = JSONResource()

app.add_route("/json", json_resource)

# For debugging. A performant way to launch is gunicorn.
if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server('localhost', 8080, app)
    httpd.serve_forever()