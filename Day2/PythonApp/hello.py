  
#!/usr/bin/python3

import flask

app = flask.Flask( __name__ )

@app.route('/', methods=['GET'])
def sayHello():
    return "Hello Python Microservice !"

app.run(host='0.0.0.0',port=80)

