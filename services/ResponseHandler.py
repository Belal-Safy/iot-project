from flask import jsonify
import flask

class ResponseHandler:
    @staticmethod
    def success_response(msg=None, data=None, status_code=200):
        res = {
            "status": status_code,
            "msg": msg,
            "data": data
        }
        
        response = flask.jsonify(res)
        return response, status_code

    @staticmethod
    def error_response(error=None, status_code=400):
        res = {
            "status": status_code,
            "error": error
        }
        
        response = flask.jsonify(res)
        return response, status_code