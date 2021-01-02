import requests
from json import dumps

url = "http://127.0.0.1:5000"


def get_jwt():
    myurl = url + "/users/login"
    body = dumps({"mailAddress": "api_user",
                  "password": "api_password"
                  })
    headers = {'Content-Type': 'applicaiton/json'}
    response = requests.request("POST", myurl, headers=headers, data=body)
    # need to strip quotation mark as they are returned as chars of string
    return response.text.lstrip('"').rstrip('"\n')


class TestAuth:
    def test_correct_auth(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_user",
                    "password": "api_password"
                    })
        headers = {'Content-Type': 'applicaiton/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 200

    def test_incorrect_usr_auth(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_incorrect",
                      "password": "api_password"
                      })
        headers = {'Content-Type': 'applicaiton/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 400

    def test_incorrect_passwd_auth(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_user",
                      "password": "api_incorrect"
                      })
        headers = {'Content-Type': 'applicaiton/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 400


class TestUsers:
    def test_get_all(self):
        myurl = url + "/users"
        token = get_jwt()
        bearer = f"Bearer {token}"
        headers = {'Authorization': bearer,
                   'Content-Type': 'application/json'}
        print(token)
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 204
