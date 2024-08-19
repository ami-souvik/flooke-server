import traceback
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery
from ..models import Like
from users.models import Persona
from utils.serializers import ModelSerializer, get_serializer
from utils.dict_handler import destruct

class LikeSerializer(ModelSerializer):
    class Meta:
        model=Like
        exclude=['created_at', 'updated_at', 'id']

    def create(self, validated_data):
        print(validated_data)
        validated_data["id"] = validated_data["user_id"]
        return super().create(validated_data)

class LikeOps(APIView):
    def get(self, request, *args, **kwargs):
        try:
            result = []
            result = []
            user_id = kwargs.get("user_id")
            posts = Post.objects.filter(user_id=OuterRef("pk")).values(
                json=JSONObject(content="content")
            )
            persona = Persona.objects.annotate(posts=ArraySubquery(posts))\
                .get(username=user_id)
            for post in persona.posts:
                result.append(post)
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
            post_id = kwargs.get("post_id")
            user_id = request.headers.get('user-id')
            serialized = LikeSerializer(data={ "post_id": post_id, "user_id": user_id })
            serialized.is_valid(raise_exception=True)
            result = ""
            try:
                like = Like.objects.get(id=str(user_id))
                like.delete()
                result = "not-liked"
            except Exception as e:
                serialized.save()
                result = "liked"
            return Response(
                result,
                status=HTTP_200_OK
            )
        except Exception as e:
            print(traceback.format_exc())
            return Response(
                f"[ERROR] While liking a post: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
