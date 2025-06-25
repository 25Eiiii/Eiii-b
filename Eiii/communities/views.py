from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from rest_framework import status

class CommunityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        posts = Post.objects.filter(category=category).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        posts = Post.objects.filter(category=category).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)