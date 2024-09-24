import jwt
import time
from django.conf import settings
from user.models import User
from django.forms.models import model_to_dict
from jwt.exceptions import ExpiredSignatureError
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED

class ApplicationAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # try:
            # In here the sleep command is used to simulate latency in the API while development
            # When deploying to production please remove or comment the following line
            time.sleep(3)
            if '/api/v1/token/' not in request.path:
                auth_token = request.headers.get("Authorization", None)
                auth_token = auth_token.replace("Bearer ", "").strip()
                payload = jwt.decode(auth_token,
                                    key=settings.SECRET_KEY,
                                    algorithms=["HS256"],
                                    options={'verify_signature': True})
                user = User.objects.get(id=payload["user_id"])
                request.user = user
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
