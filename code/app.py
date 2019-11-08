from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenthicate, identity

app = Flask(__name__)
app.secret_key = 'JyjJJj7SK4YQMpt0ClCAI2dJO6wgx9XggoP6J32BMWrCSOLeI8eqySZpX0580fJ'
api = Api(app)

jwt = JWT(app, authenthicate, identity)  #Esto crea un nuevo endpoint /auth

students = []


class Student(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('lastname', type=str, required=True, help="Name cannot be blank!")

    parser.add_argument('grades', action='append') #Para listas debo pasar el argumento action='append'

    @jwt_required()
    def get(self, name):
        student = next(filter(lambda x: x['name'] == name, students), None)
        return {'student': student}, 200 if student else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, students), None):
            return {'message': 'An student whit this name {} already exists'.format(name)}, 400

        data = Student.parser.parse_args()

        student = {'name': name, 'lastname': data['lastname'],  'grades': data['grades']}
        students.append(student)
        return student, 201

    def delete(self, name):
        global students
        students = list(filter(lambda x: x['name'] != name, students))
        return{'message': 'Student deleted.'}


    def put(self, name):

        data = Student.parser.parse_args()

        student = next(filter(lambda x: x['name'] == name, students), None)
        if student is None:
            student = {'name': name, 'lastname': data['lastname'],  'grades': data['grades']}
            students.append(student)
        else:
            student.update(data)
        return student


class StudentList(Resource):
    def get(self):
        return {'students': students}

api.add_resource(Student, '/student/<string:name>') #http://127.0.0.1:5000/student/<string:name> replace to app.route
api.add_resource(StudentList, '/students')

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # important to mention debug=True
