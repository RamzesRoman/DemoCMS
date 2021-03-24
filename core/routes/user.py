from flask import Flask, redirect, render_template, make_response, escape,request, jsonify, Blueprint
from core.models.user import User
from core.protected import protected
import json

app=Blueprint('user',__name__, template_folder='public_html')

@app.route('/api/users',methods=['GET'])
@protected('admin')
def enumerate():
    user=User()
    if not request.args.get('search') is None:
      search=json.loads(request.args.get('search'))
    else:
      search=None
    start=request.args.get('start')
    limit=request.args.get('limit')
    data=user.enumerate(search=search,start=start,limit=limit)
    return jsonify(data)

@app.route('/api/user',methods=['POST'])
@protected('admin')
def create():
    data=request.json
    user=User()
    id=user.create(data)
    return jsonify({"id":id})

@app.route('/api/user/<id>',methods=['GET'])
@protected('admin')
def read(id):
    data=request.json
    user=User()
    data=user.read(id)
    return jsonify(data)

@app.route('/api/user/<id>',methods=['PUT'])
@protected('admin')
def update(id):
    data=request.json
    user=User()
    id=user.update(id,data)
    return jsonify({"result":"ok"})

@app.route('/api/user/<id>',methods=['DELETE'])
@protected('admin')
def delete(id):
    user=User()
    data=user.delete(id)
    return jsonify({"result":"ok"})


@app.route('/admin/user.html',methods=['POST'])
@protected('admin')
def login():
    try:
      data={}
      if request.form["password"] != request.form["password2"]:
          raise Exception("Паролі не співпадають")
      if request.form["name"] == "":
          raise Exception("Ім'я не може бути пустим")
      if request.form["password"] =="":
          raise Exception("Пароль не може бути пустим")
      if len(request.form["password"]) < 6:
          raise Exception("Пароль не може менше 6ти знаків")
      if request.form["password"]:
          data["pass"]=request.form["password"]
      u=User()
      data["name"]=request.form["name"]
      user=u.update(request.args.get("id"), data)
      return make_response(redirect("/admin/users.html"))

    except Exception as e:
      print(e)
      return make_response(render_template("admin/user.html",error=str(e),params=request.args.to_dict()))
