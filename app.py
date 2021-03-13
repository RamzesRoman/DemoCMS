#!/usr/bin/python3

from flask import Flask, g, session, request, render_template, make_response, send_from_directory
from core.protected import protected
from core.models.user import User
from core.models.session import Session
from core.routes.user import app as user
from core.routes.authorization import app as authorization


app = Flask(__name__,template_folder='public_html')
app.register_blueprint(user)
app.register_blueprint(authorization)

#u=User()
#u.create({"name":"Nikolay","email":"test2@mail.com","pass":"qwerty1234"})

@app.before_request
def load_user():
    user_data={}
    if "sess_id" in request.cookies:
        sess=Session()
        s=sess.read(request.cookies["sess_id"])
        if not s is None and "user_id" in s:
          user=User()
          user_data=user.read(s["user_id"])
        pass
    g.user = user_data

@app.route('/static/css/<path:path>')
def send_static(path):
    return send_from_directory('public_html/css/', path)

@app.route('/')
def index_page():
    return make_response(render_template("index.html"))

@app.route('/<page>.html')
def get_page(page):
    return make_response(render_template(page + ".html"))


@app.route('/admin/<page>.html')
@protected
def get_admin_page(page):
    return make_response(render_template("admin/" +page + ".html"))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
