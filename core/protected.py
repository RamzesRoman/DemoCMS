from functools import wraps
from flask import g, request, redirect, url_for

def protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(" [x] User: " + str(g.user.get("id")))
        if g.user.get("id") is None:
            return redirect('/login.html?u=' + request.url)
        return f(*args, **kwargs)
    return decorated_function
