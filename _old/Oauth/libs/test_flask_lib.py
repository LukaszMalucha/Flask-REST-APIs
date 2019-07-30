from flask import g

def function_accessing_global():
    print(g.token)
