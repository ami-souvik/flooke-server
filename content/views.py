from django.contrib import auth
from django.forms.models import model_to_dict
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Content
from basic_auth.models import User
from .serializers import ContentSerializer
from utils.dict_handler import destruct

class ContentView(APIView):
    """Basic ListView implementation to get the posted contents list."""
    model = Content
    pagination = 10
    
    def get(self, request):
        try:
            result = []
            posts = Content.objects.all().order_by('-created_at')[:10]
            for p in posts:
                result.append(p.to_dict())
            return Response(
                result,
                status=HTTP_200_OK
            )
        except Exception as e:
            return Response(
                f"[ERROR] While fetching posts: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
    
    def post(self, request):
        try:
            user = request.META["context"]["user"]
            request.data["owner"] = user.id
            serialized = ContentSerializer(data=request.data)
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

