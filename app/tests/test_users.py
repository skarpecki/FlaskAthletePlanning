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
    def test_correct_auth_code(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_user",
                     "password": "api_password"
                    })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 200

    def test_incorrect_usr_auth_code(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_incorrect",
                      "password": "api_password"
                      })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 400

    def test_incorrect_passwd_auth_code(self):
        myurl = url + "/users/login"
        body = dumps({"mailAddress": "api_user",
                      "password": "api_incorrect"
                      })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 400

    def test_get_code(self):
        myurl = url + "/users/login"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 200

    def test_get_content(self):
        myurl = url + "/users/login"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        rcvd_data = eval(response.text)
        assert_data = dict({"role": "coach", "userID": 21})
        assert rcvd_data == assert_data

class TestUsers:
    def test_get_all(self):
        myurl = url + "/users"
        token = get_jwt()
        bearer = f"Bearer {token}"
        headers = {'Authorization': bearer,
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 200


if __name__ == '__main__':
    pass
