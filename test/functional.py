import unittest
import requests
import json

host = "http://localhost:8080"


class FunctionalTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user(self):
        user = {'username': 'test_user_999', 'email': 'bob@example.com'}

        users = requests.get(host + "/users/").json()
        if user['username'] in users:
            resp = requests.delete(host + "/users/" + user['username'])
            self.assertEqual(200, resp.status_code, resp.text)
            users = requests.get(host + "/users/")
        self.assertNotIn(user['username'], users)

        resp = requests.post(host + '/users/', data=json.dumps(user))
        self.assertEqual(201, resp.status_code, resp.text)

        resp = requests.post(host + '/users/', data=json.dumps(user))
        self.assertNotEqual(200, resp.status_code, "shouldn't allow multiple of the same username")
        users = requests.get(host + "/users/").json()
        self.assertIn(user['username'], users)

        resp = requests.get(host + '/users/' + user['username'])
        self.assertEqual(200, resp.status_code, resp.text)
        self.assertEqual(user, resp.json())

        resp = requests.delete(host + "/users/" + user['username'])
        self.assertEqual(200, resp.status_code, resp.text)

        resp = requests.delete(host + "/users/" + user['username'])
        self.assertNotEqual(200, resp.status_code, "should complain if user is gone")

        users = requests.get(host + "/users/").json()
        self.assertNotIn(user['username'], users)

if __name__ == "__main__":
    unittest.main()
