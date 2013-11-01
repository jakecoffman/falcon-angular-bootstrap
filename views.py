import json
import falcon
from models import User


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
