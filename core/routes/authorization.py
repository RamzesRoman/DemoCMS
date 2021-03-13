from flask import Flask, render_template, make_response, escape,request, jsonify, Blueprint, redirect
from core.models.user import User
from core.models.session import Session
import json

app=Blueprint('authorization',__name__, template_folder='public_html')


@app.route('/login',methods=['POST'])
def login():
    email=request.form["email"]
    password=request.form["password"]
    u=User()
    user=u.login(email,password)
    if user is None:
      return make_response(render_template("login.html"))
    print(user)
    sess=Session()
    s=sess.create({"user_id":user["id"]})
    resp=make_response(redirect("index.html"))
    resp.set_cookie('sess_id', str(s["id"]))
    return resp

