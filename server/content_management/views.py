import traceback
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from users.models import Persona
from utils.serializers import get_serializer
from utils.dict_handler import destruct

# Create your views here.
class CreatePost(APIView):
    def get(self, request, *args, **kwargs):
        try:
            posts = []
            for u in Post.objects.all():
                posts.append(model_to_dict(u))
            return Response(
                posts,
                status=HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
    
    def post(self, request, *args, **kwargs):
        try:
            user_id, _rest = destruct(request.data, keys=['user_id', '*'])
            _persona = Persona.objects.get(username=user_id)
            serialized = get_serializer(Post, data={ user_id: _persona, **_rest })
            serialized.is_valid(raise_exception=True)
            return Response(
                model_to_dict(serialized.save()),
                status=HTTP_200_OK
            )
        except Exception as e:
            print(traceback.format_exc())
            return Response(
                f"[ERROR] While creating user: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
