from flask import Flask, render_template, make_response, escape,request, jsonify, Blueprint
from core.models.access import Access
from core.protected import protected
import json

app=Blueprint('access',__name__, template_folder='public_html')

@app.route('/api/accesses',methods=['GET'])
@protected('admin')
def enumerate():
    access=Access()
    if not request.args.get('search') is None:
      search=json.loads(request.args.get('search'))
    else:
      search=None
    start=request.args.get('start')
    limit=request.args.get('limit')
    data=access.enumerate(search=search,start=start,limit=limit)
    return jsonify(data)

@app.route('/api/access',methods=['POST'])
@protected('admin')
def create():
    data=request.json
    access=Access()
    id=access.create(data)
    return jsonify({"id":id})

@app.route('/api/access/<id>',methods=['GET'])
@protected('admin')
def read(id):
    data=request.json
    access=Access()
    data=access.read(id)
    return jsonify(data)

@app.route('/api/access/<id>',methods=['PUT'])
@protected('admin')
def update(id):
    data=request.json
    access=Access()
    id=access.update(id,data)
    return jsonify({"result":"ok"})

@app.route('/api/access/<id>',methods=['DELETE'])
@protected('admin')
def delete(id):
    access=Access()
    data=access.delete(id)
    return jsonify({"result":"ok"})
