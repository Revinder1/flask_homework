from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from config import PG_DSN_ALC
from db.models import Post, User
from errors import HttpError

engine = create_engine(PG_DSN_ALC)
Session = sessionmaker(bind=engine)


def get_post(session: Session, post_id: int):
    post = session.query(Post).get(post_id)
    if post is None:
        raise HttpError(404, 'Post not found')
    return post


class PostView(MethodView):

    def get(self, post_id: int):
        with Session() as session:
            post = get_post(session, post_id)
            return jsonify({'title': post.title, 'created_at': post.created_at.isoformat(), 'user_id': post.user_id})

    def post(self):
        with Session() as session:
            post = Post(title=request.json['title'], description=request.json['description'],
                        user_id=request.json['user_id'])
            session.add(post)
            session.commit()
            return {'post': post.title, 'user_id': post.user_id}

    def delete(self, post_id: int):
        with Session() as session:
            post = get_post(session, post_id)
            session.delete(post)
            session.commit()
            return {'status': 'post was successfully deleted'}


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(User).get(user_id)
            return jsonify({'user_id': user.id, 'name': user.name})

    def post(self):
        with Session() as session:
            user = User(name=request.json['name'], password=request.json['password'])
            session.add(user)
            session.commit()
            return {'user_id': user.id, 'name': user.name}


    # def create_user(session: Session, name: str, password: str):
    #     try:
    #         user = User(name, password)
    #         session.add(user)
    #         session.commit()
    #     except IntegrityError as e:
    #         return HttpError