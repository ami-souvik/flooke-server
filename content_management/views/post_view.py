import traceback
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery
from ..models import Post
from users.models import Persona
from utils.serializers import get_serializer
from utils.dict_handler import destruct

class PostOps(APIView):
    def get(self, request, *args, **kwargs):
        try:
            result = []
            posts = Post.objects.all()
            for p in posts:
                result.append(model_to_dict(p))
            return Response(
                result,
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While fetching posts: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
    
    def post(self, request, *args, **kwargs):
        try:
            user_id, _rest = destruct(request.data, keys=['user_id', '*'])
            _persona = Persona.objects.get(username=user_id)
            _rest["user_id"] = _persona.id
            serialized = get_serializer(Post, data=_rest)
            serialized.is_valid(raise_exception=True)
            return Response(
                model_to_dict(serialized.save()),
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While creating post: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )

class GetPostsByUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            result = []
            user_id = kwargs.get("user_id")
            posts = Post.objects.filter(user_id=OuterRef("pk")).values(
                json=JSONObject(content="content")
            )
            persona = Persona.objects.annotate(posts=ArraySubquery(posts))\
                .get(username=user_id)
            for post in persona.posts:
                result.append(post)
            return Response(
                result,
                status=HTTP_200_OK
            )
        except Exception as e:
            print(traceback.format_exc())
            return Response(
                f"[ERROR] While fetching posts: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
