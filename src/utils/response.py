from flask import jsonify


class JsonResponse:
    HTTP_CODE_OK = 200
    HTTP_CODE_CREATED = 201
    HTTP_CODE_DELETED = 204
    HTTP_CODE_UNAUTHORIZED = 401
    HTTP_CODE_BAD_REQUEST = 400
    HTTP_CODE_FORBIDDEN = 403
    HTTP_CODE_NOT_FOUND = 404
    HTTP_CODE_CONFLICT = 409
    HTTP_CODE_SERVER_ERROR = 500
    HTTP_CODE_NOT_IMPLEMENTED = 501

    def success(self, data: dict = None):
        return self._response(self.HTTP_CODE_OK, data)

    def created(self, data: dict = None):
        return self._response(self.HTTP_CODE_CREATED, data)

    def deleted(self, data: dict = None):
        return self._response(self.HTTP_CODE_DELETED, data)

    def bad_request(self, data: dict = None):
        return self._response(self.HTTP_CODE_BAD_REQUEST, data)

    def not_found(self, data: dict = None):
        return self._response(self.HTTP_CODE_NOT_FOUND, data)

    def unauthorized(self, data: dict = None):
        return self._response(self.HTTP_CODE_UNAUTHORIZED, data)

    def forbidden(self, data: dict = None):
        return self._response(self.HTTP_CODE_FORBIDDEN, data)

    def conflict(self, data: dict = None):
        return self._response(self.HTTP_CODE_CONFLICT, data)

    def server_error(self, data: dict = None):
        return self._response(self.HTTP_CODE_SERVER_ERROR, data)

    def not_implemented(self, data: dict = None):
        return self._response(self.HTTP_CODE_NOT_IMPLEMENTED, data)

    @classmethod
    def _response(cls, code: int, data: dict = None):
        if data is not None:
            return jsonify(data), code
        return '', code


json_response = JsonResponse()
