from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

students = []


class Student(Resource):

    def get(self, name):
        for student in students:
            if student['name'] == name:
                return student
        return {'student': None}

    def post(self, name):
        student = {'name': name, 'lastname': 'Juanes',  'grades': [20,20,20]}
        students.append(student)
        return student

api.add_resource(Student, '/student/<string:name>') #http://127.0.0.1:5000/student/<string:name> replace to app.route
app.run(port=5000)
