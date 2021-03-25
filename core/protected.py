from functools import wraps
from flask import g, request, redirect, url_for
from core.models.access import Access

def protected(access=""):
  def protected_decorator(f):
      @wraps(f)
      def decorated_function(*args, **kwargs):
          if not g.user is None:
              if not g.user.get("id") is None:
                  try:
                      a=Access()
                      access_data=a.read(g.user.get("access_id"))
                      print(" [x] Access: " + str(access_data))
                      print(" [x] User: " + str(g.user.get("id")))
                      print(" [x] User access: " + str(g.user.get("access_id")))

                      if access_data.get('name') == access:
                          return f(*args, **kwargs)
                  except:
                      pass
          return redirect('/login.html?u=' + request.url)
          
      return decorated_function
  return protected_decorator