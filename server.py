from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from db.base import Base
from errors import HttpError
from views import PostView, engine, UserView

app = Flask('app')
bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    response = jsonify({
        'status': 'error',
        'reason': error.message
    })

    response.status_code = error.status_code
    return response


Base.metadata.create_all(engine)


post_view = PostView.as_view('posts')
user_view = UserView.as_view('users')
app.add_url_rule('/posts/', view_func=post_view, methods=['POST'])
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'DELETE'])
app.add_url_rule('/posts/<int:post_id>', view_func=post_view, methods=['GET', 'DELETE'])


app.run()
