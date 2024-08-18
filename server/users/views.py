from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Persona

# Create your views here.
class UserView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            users = []
            for u in Persona.objects.all():
                users.append(model_to_dict(u))
            return Response(
                users,
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        try:
            serialized = UserSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            return Response(
                model_to_dict(serialized.save()),
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
