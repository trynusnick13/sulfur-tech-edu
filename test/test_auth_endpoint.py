import os

import pytest
from app.asgi import get_app
from fastapi.testclient import TestClient

from app.tools.get_database import get_db
from sqlalchemy import create_engine
from app.Config.database import Base
from sqlalchemy.orm import sessionmaker
from app.Config.application import BASEDIR

from image_data import image

SQLALCHEMY_DATABASE_URL = 'sqlite:///'+BASEDIR+'../../SqlitePyTest.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='module', autouse=True)
def client():
    application = get_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as client:
        yield client

    os.remove('/home/nuznhy/PycharmProjects/FastApiProject/app/SqlitePyTest.db')


def test_ready(client):
    response = client.get('/api/ready')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


class TestAuth:
    @pytest.mark.parametrize('reg_data',
                             [
                                 pytest.param(
                                     {
                                         "email": "nuznhy@gmail.com",
                                         "password": "12345ABAMAsd",
                                         "repeat_password": "12345ABAMAsd",
                                         "first_name": "Fname",
                                         "last_name": "Lname"
                                     },
                                     id='Registration success'
                                 ),
                                 pytest.param(
                                     {
                                         "email": "nuznhy@gmail.com",
                                         "password": "12345ABAMAsd",
                                         "repeat_password": "12345ABAMAsd",
                                         "first_name": "Fname",
                                         "last_name": "Lname"
                                     },
                                     id='Registration fail 1',
                                     marks=pytest.mark.xfail(reason='Email is taken')
                                 ),
                                 pytest.param(
                                     {
                                         "email": "nuznhy@gmail.com",
                                         "password": "12345ABAMAsd",
                                         "repeat_password": "ABAMAsd",
                                         "first_name": "Fname",
                                         "last_name": "Lname"
                                     },
                                     id='Registration fail 2',
                                     marks=pytest.mark.xfail(reason="Password and Repeated password don't match")
                                 ),
                             ])
    def test_auth_register(self, client, reg_data):
        response = client.post('/auth/register', json=reg_data)
        json = response.json()
        print(json)
        assert response.status_code == 200
        assert 'access_token' in json
        assert 'token_type' in json

    @pytest.mark.parametrize('login_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            id='Login success'
        ),
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAM"
            },
            id='Login fail 1',
            marks=pytest.mark.xfail(reason='Wrong password')
        ),
        pytest.param(
            {
                "email": "com",
                "password": "12345ABAMAsd"
            },
            id='Login fail 2',
            marks=pytest.mark.xfail(reason='Wrong email')
        ),
    ])
    def test_login(self, client, login_data):
        response = client.post('/auth/login', json=login_data)
        json = response.json()
        print(json)
        assert response.status_code == 200
        assert 'access_token' in json


class TestUser:
    @pytest.mark.parametrize('login_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            id='Show self success'
        ),
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAM"
            },
            id='Show self fail',
            marks=pytest.mark.xfail(reason='No auth')
         )
    ])
    def test_show_self(self, client, login_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.get('/user/profile',
                              headers={'Authorization': 'Bearer ' + access_token})
        assert 'user' in response.json()

    @pytest.mark.parametrize('login_data, json_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                'image': image
            },
            id='Avatar upload success'
        )
    ])
    def test_avatar_upload(self, client, login_data, json_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.put('/user/avatar-upload',
                              json=json_data,
                              headers={'Authorization': 'Bearer ' + access_token})
        assert 'user' in response.json()


class TestCourses:
    @pytest.mark.parametrize('login_data, json_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_name": "Test Course",
                "course_price": 10.0,
                "course_description": "Some description",
                "image": image
            },
            id='Create course success'
        ),
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_name": "",
                "course_price": 10.0,
                "course_description": "Some description",
                "image": image
            },
            id='Create course fail',
            marks=pytest.mark.xfail(reason='Empty name')
        )
    ])
    def test_course_create(self, client, login_data, json_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.post('/course/create',
                               json=json_data,
                               headers={'Authorization': 'Bearer ' + access_token})
        assert 'course' in response.json()
        assert response.status_code == 200

    @pytest.mark.parametrize('course_id', [
        pytest.param(
            1,
            id='Course show id success'
        ),
        pytest.param(
            2,
            id='Course show id fail',
            marks=pytest.mark.xfail(reason='404')
        )
    ])
    def test_course_get_id(self, client, course_id):
        response = client.get('/course/get-id/{}'.format(course_id))
        assert 'course' in response.json()
        assert response.status_code == 200

    def test_course_get_all(self, client):
        response = client.get('/course/all')
        assert 'courses' in response.json()
        assert response.status_code == 200

    @pytest.mark.parametrize('creator_id', [
        pytest.param(1, id='Correct show by creator')
    ])
    def test_get_by_creator_id(self, client, creator_id):
        response = client.get('/course/get-by-creator-id/{}'.format(creator_id))
        assert 'courses' in response.json()
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, json_data, course_id', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_name": "Updated Test Course",
                "course_price": 15.0,
                "course_description": "Updated some description",
                "image": image
            },
            1,
            id='Course update'
        )
    ])
    def test_course_update(self, client, login_data, json_data, course_id):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.patch('/course/update/{}'.format(course_id),
                               json=json_data,
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, json_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_id": 1
            },
            id='Subscribe success'
        ),
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_id": 2
            },
            id='Subscribe fail',
            marks=pytest.mark.xfail(reason='404')
        )
    ])
    def test_course_subscribe(self, client, login_data, json_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.post('/course/subscribe',
                               json=json_data,
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            id='Correct show my courses'
        )
    ])
    def test_get_my_courses(self, client, login_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.get('/course/my-subscribed',
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, course_id', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            1,
            id='Correct show my students'
        )
    ])
    def test_get_students_of_my_course(self, client, login_data, course_id):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.get('/course/students/{}'.format(course_id),
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, json_data, course_id', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                'rate': 5
            },
            1,
            id='Correct rate'
        )
    ])
    def test_course_rate(self, client, login_data, json_data, course_id):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.post('/course/rate/{}'.format(course_id),
                               json=json_data,
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, json_data', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_id": 1
            },
            id='Unsubscribe success'
        ),
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            {
                "course_id": 2
            },
            id='Subscribe fail',
            marks=pytest.mark.xfail(reason='404')
        )
    ])
    def test_unsubscribe(self, client, login_data, json_data):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.delete('/course/unsubscribe',
                               json=json_data,
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200

    @pytest.mark.parametrize('login_data, course_id', [
        pytest.param(
            {
                "email": "nuznhy@gmail.com",
                "password": "12345ABAMAsd"
            },
            1,
            id='Unsubscribe success'
        )
    ])
    def test_course_delete(self, client, login_data, course_id):
        response_auth = client.post('/auth/login', json=login_data)
        access_token = response_auth.json().get('access_token')
        response = client.delete('/course/delete/{}'.format(course_id),
                               headers={'Authorization': 'Bearer ' + access_token})
        assert response.status_code == 200