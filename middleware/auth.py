import jwt
from django.conf import settings
from basic_auth.models import User
from django.forms.models import model_to_dict
from jwt.exceptions import ExpiredSignatureError
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED

class ApplicationAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # try:
            if '/api/v1/token/' not in request.path and '/api/v1/auth/users/' not in request.path:
                auth_token = request.headers.get("Authorization", None)
                auth_token = auth_token.replace("Bearer ", "").strip()
                payload = jwt.decode(auth_token,
                                    key=settings.SECRET_KEY,
                                    algorithms=["HS256"],
                                    options={'verify_signature': True})
                user = User.objects.get(id=payload["user_id"])
                req_meta = dict(request.META)
                req_meta['context'] = {
                    "user": user
                }
                request.META = req_meta
            response = self.get_response(request)
            return response
        # except ExpiredSignatureError as e:
        #     return Response(
        #         { "message": "[ERROR] Token has been expired" },
        #         status=HTTP_401_UNAUTHORIZED
        #     )
        # except Exception as e:
        #     return Response(
        #         { "message": "Internal server error" },
        #         status=HTTP_500_INTERNAL_SERVER_ERROR
        #     )
