from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.dict_handler import destruct
from .serializers import UserSerializer

# Create your views here.
class AuthView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = request.META["context"]["user"]
            username, first_name, last_name, email = destruct(dict=model_to_dict(user), keys=["username", "first_name", "last_name", "email"])
            return Response(
                {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                },
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While fetching user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                model_to_dict(serializer.save()),
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
