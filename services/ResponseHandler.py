from flask import jsonify

class ResponseHandler:
    @staticmethod
    def success_response(msg=None, data=None, status_code=200):
        response = {
            "status": status_code,
            "msg": msg,
            "data": data
        }
        return jsonify(response), status_code

    @staticmethod
    def error_response(error=None, status_code=400):
        response = {
            "status": status_code,
            "error": error
        }
        return jsonify(response), status_code
