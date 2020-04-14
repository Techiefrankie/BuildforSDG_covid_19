from flask import Flask, jsonify, request, make_response
from flask_restful import Api
import src.estimator as estimator
import time
from simplexml import dumps

# define the application
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
log_file = "logs.txt"


@app.route('/api/v1/on-covid-19/', methods=['POST'])
def post():
    # get the json string from the request body
    req_data = request.get_json()
    req_time = int(round(time.time() * 1000))
    route = request.path
    rsp = process(req_time, route, req_data)
    return jsonify(rsp)


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def post_xml():
    # get the json string from the request body
    req_data = request.get_json()
    req_time = int(round(time.time() * 1000))
    route = request.path
    rsp = process(req_time, route, req_data)
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': rsp}))
    resp.headers.extend({"mimetype": "text/xml"})
    return resp


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def post_json():
    # get the json string from the request body
    req_data = request.get_json()
    req_time = int(round(time.time() * 1000))
    route = request.path
    rsp = process(req_time, route, req_data)
    return jsonify(rsp)


def process(req_time, route, req_data):
    try:
        # pass the request data to the estimator function
        rsp = estimator.estimator(req_data)
        # return a json response to the browser
        rsp_time = int(round(time.time() * 1000))
        diff_sec = (rsp_time - req_time) / 1000
        log = str(req_time) + "\t\t" + route + "\t\t done in " + str(diff_sec) + " seconds\n"
        append_log(log)
    except(TypeError, ValueError):
        error = {
            "message": "Invalid data passed"
        }
        return error
    return rsp


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def logs():
    logging = ""
    try:
        f = open(log_file, mode='rt', encoding='utf-8')
        for line in f.read():
            logging += line
    except FileNotFoundError:
        error = {
            "message": "Log is currently empty"
        }
        return jsonify(error)
    finally:
        f.close()
    return logging


def append_log(log):
    f = open(log_file, mode='at', encoding='utf-8')
    f.write(log)
    f.close()


if __name__ == "__main__":
    app.run()
