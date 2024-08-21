from django.contrib import auth
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from utils.dict_handler import destruct

class CommentView(APIView):
    """Basic ListView implementation to get the posted contents list."""
    model = Comment
    pagination = 10
    
    def get(self, request, *args, **kwargs):
        try:
            result = []
            user = request.META["context"]["user"]
            content_id = kwargs.get("content_id")
            comments = Comment.objects.all_by_content(user_id=user.id, content_id=content_id)
            for c in comments:
                result.append(model_to_dict(c))
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
            user = request.META["context"]["user"]
            request.data["owner"] = user.id
            content_id = kwargs.get("content_id")
            request.data["content"] = content_id
            serialized = CommentSerializer(data=request.data)
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

