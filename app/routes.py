from flask import make_response, jsonify

from app import app

@app.route('/')
def ping():
    headers = {'Content-Type': 'application/json'}
    response = {
        'meta': {
            'project': 'NLIMDb',
            'description': 'Natural Language Interface to Movie Database',
            'authors': [    
                'Ali Sanaknaki',
                'Finn Lao',
                'Youssef El-Hasbani'
            ]
        }
    }

    return make_response(jsonify(response), 200, headers)




@app.errorhandler(400)
def bad_request(e):
    headers = {'Content-Type': 'application/json'}
    response = {
        'error': {
            'status' : '400',
            'message' : 'bad request'
        }
    }
    return make_response(jsonify(response), 400, headers)

@app.errorhandler(404)
def page_not_found(e):
    headers = {'Content-Type': 'application/json'}
    response = {
        'error': {
            'status' : '404',
            'message' : 'resource not found'
        }
    }
    return make_response(jsonify(response), 404, headers)

@app.errorhandler(500)
def server_error(e):
    headers = {'Content-Type': 'application/json'}
    response = {
        'error': {
            'status' : '500',
            'message' : 'server error'
        }
    }
    return make_response(jsonify(response), 500, headers)