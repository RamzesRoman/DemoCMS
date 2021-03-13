from flask import Flask, render_template, make_response, escape,request, jsonify, Blueprint
from core.models.user import User
from core.protected import protected
import json

app=Blueprint('user',__name__, template_folder='public_html')

@app.route('/api/users',methods=['GET'])
#@protected
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
#@protected
def create():
    data=request.json
    user=User()
    id=user.create(data)
    return jsonify({"id":id})

@app.route('/api/user/<id>',methods=['GET'])
#@protected
def read(id):
    data=request.json
    user=User()
    data=user.read(id)
    return jsonify(data)

@app.route('/api/user/<id>',methods=['PUT'])
#@protected
def update(id):
    data=request.json
    user=User()
    id=user.update(id,data)
    return jsonify({"result":"ok"})

@app.route('/api/user/<id>',methods=['DELETE'])
#@protected
def delete(id):
    user=User()
    data=user.delete(id)
    return jsonify({"result":"ok"})
