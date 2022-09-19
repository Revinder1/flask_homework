import requests

from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from flask.views import MethodView
from flask_bcrypt import Bcrypt
import pydantic
import typing

from sqlalchemy.orm import sessionmaker

import config



def hash_password(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()


class HttpError(Exception):

    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


class CreateUser(pydantic.BaseModel):
    name: str
    password: str


class PatchUser(pydantic.BaseModel):
    name: typing.Optional
    password: str


def validate(model, raw_data: dict):
    try:
        return model(**raw_data).dict()
    except pydantic.ValidationError as error:
        raise HttpError(400, error.errors())


app = Flask('app')
bcrypt = Bcrypt(app)


engine = create_engine(config.PG_DSN_ALC)
Session = sessionmaker(bind=engine)


def get_user(session: Session, user_id: int):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'User not found')
    return user


Base.metadata.create_all(engine)


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify({'name': user.name, 'created_at': user.created_at.isoformat()})

        pass

    def post(self):
        validated = validate(CreateUser, request.json)
        with Session() as session:
            user = User(name=validated['name'], password=hash_password(validated['password']))
            session.add(user)
            session.commit()
            return {'id': user.id}

    def patch(self, user_id):
        validated = validate(PatchUser, request.json)

        with Session() as session:
            user = get_user(session, user_id)
            if validated.get('name'):
                user.name = validated['name']
            if validated .get('password'):
                user.password = hash_password(validated['password'])
            session.add(user)
            session.commit()
            return {
                'status': 'success'
            }

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return {'status': 'access'}



user_view = UserView.as_view('users')
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])


app.run()
