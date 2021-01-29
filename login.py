#!/usr/bin/env python3
import cgi
import cgitb
cgitb.enable()

from templates import login_page, secret_page, after_login_incorrect
import secret
import os
import sys
from http.cookies import SimpleCookie

s = cgi.FieldStorage()
username = s.getfirst("username")
password = s.getfirst("password")

form_ok = username == secret.username and password == secret.password

c = SimpleCookie(os.environ["HTTP_COOKIE"])
c_username = None
c_password = None
if c.get("username"):
    c_username = c.get("username").value
if c.get("password"):
    c_password = c.get("password").value

cookie_ok = c_username == secret.username and c_password == secret.password

if cookie_ok:
    username = c_username
    password = c_password

print("Content-Type: text/html")
if form_ok:
    #set cookie info
    print(f"Set-Cookie: username={username}")
    print(f"Set-Cookie: password={password}")

print()

if not username and not password:
    print(login_page())
elif username == secret.username and password == secret.password:
    # print("login correct!")
    posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
    if posted_bytes:
        posted = sys.stdin.read(int(posted_bytes))
        print(f"<p> POSTED: <pre>")
        print(posted)
        for line in posted.splitlines():
            print(line)
        print("</pre></p>")
    print(secret_page(username, password))
else:
    print(after_login_incorrect())
    print("username = ", username)
    print("password = ", password)