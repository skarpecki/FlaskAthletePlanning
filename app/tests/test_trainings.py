import requests
from json import dumps
import random
from datetime import date

url = "http://127.0.0.1:5000"


def get_jwt():
    myurl = url + "/users/login"
    body = dumps({"mailAddress": "api_user",
                  "password": "api_password"
                  })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", myurl, headers=headers, data=body)
    # need to strip quotation mark as they are returned as chars of string
    return response.text.lstrip('"').rstrip('"\n')


class TestTrainings:
    def test_create_code(self):
        myurl = url + "/trainings"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        body = dumps({'date': '2021-12-31',
                      'athleteID': '8'})
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 201

    def test_get_by_id_code(self):
        myurl = url + "/trainings/1"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 200

    def test_code_modify(self):
        myurl = url + "/trainings/1"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        random.seed()
        year = int(random.random() * 10 + 2021)  # produces int in range 2021, 2031, change in 2022
        month = random.randint(1, 12)  # another way of producing random numbers
        day = random.randint(1, 28)  # end no. is 28 as in February anything more may cause an error
        # randomized date as same date provided as assigned to training will raise validation error and 400 http code
        tr_date = date(year, month, day)
        feedback = "test_feedback"
        body = dumps({"feedback": feedback,
                      "date": str(tr_date)})
        response = requests.request("PUT", myurl, headers=headers, data=body)
        assert response.status_code == 201

    def test_code_get_by_query(self):
        myurl = url +"/trainings?trainingID=1"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 200


class TestExercises:
    def test_code_create(self):
        myurl = url + "/trainings/1/exercises"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        sets = random.randint(1, 20)
        reps = random.randint(1, 20)
        rpe = random.randint(1, 10)
        body = dumps({"exerciseName": "Squat", "sets": sets, "reps": reps, "rpe": rpe})
        response = requests.request("POST", myurl, headers=headers, data=body)
        assert response.status_code == 201

    def get_exercises(self):
        myurl = url + "/trainings/1/exercises"
        token = get_jwt()
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        return response

    def test_code_get_exercises(self):
        response = self.get_exercises()
        assert response.status_code == 200

    def test_code_modify_exercise(self):
        d1 = eval(self.get_exercises().text)[0]
        exercise_id = d1['exerciseID']
        token = get_jwt()
        myurl = url + "/trainings/1/exercises/{}".format(exercise_id)
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        sets = random.randint(1, 20)
        reps = random.randint(1, 20)
        rpe = random.randint(1, 10)
        body = dumps({"exerciseName": "Squat", "sets": sets, "reps": reps, "rpe": rpe})
        response = requests.request("PUT", myurl, headers=headers, data=body)
        assert response.status_code == 201

    def test_code_get_exercise_id(self):
        d1 = eval(self.get_exercises().text)[0]
        exercise_id = d1['exerciseID']
        token = get_jwt()
        myurl = url + "/trainings/1/exercises/{}".format(exercise_id)
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("GET", myurl, headers=headers)
        assert response.status_code == 200

    def test_code_delete_exercise(self):
        d1 = eval(self.get_exercises().text)[0]
        exercise_id = d1['exerciseID']
        token = get_jwt()
        myurl = url + "/trainings/1/exercises/{}".format(exercise_id)
        headers = {'Authorization': 'Bearer {}'.format(token),
                   'Content-Type': 'application/json'}
        response = requests.request("Delete", myurl, headers=headers)
        assert response.status_code == 200


if __name__ == "__main__":
    pass

