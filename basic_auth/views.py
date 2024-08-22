import structlog
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.dict_handler import destruct
from .serializers import UserSerializer, UpdateUserSerializer
from .models import User

logger = structlog.get_logger(__name__)

# Create your views here.
class AuthView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = request.META["context"]["user"]
            return Response(
                user.to_dict(),
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
                serializer.save().to_dict(),
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )

class UpdateUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.META["context"]["user"]
            serializer = UpdateUserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                serializer.save().to_dict(),
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
