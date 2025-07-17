from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like, Scrap
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class CommunityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category):
        posts = Post.objects.filter(category=category).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})  
        return Response(serializer.data)
    
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # 현재 로그인한 사용자가 작성한 글만 삭제 가능
    #     return Post.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            return Response({'message': '좋아요가 취소되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '좋아요가 추가되었습니다.'}, status=status.HTTP_201_CREATED)

class LikedPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user.id)

        liked_posts = Post.objects.filter(likes__user=request.user).order_by('-created_at')
        serializer = PostSerializer(liked_posts, many=True, context={'request': request})
        return Response(serializer.data)


class ScrappedPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        scrapped_posts = Post.objects.filter(scraps__user=request.user).order_by('-created_at')
        serializer = PostSerializer(scrapped_posts, many=True, context={'request': request})
        return Response(serializer.data)

class ScrapView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        scrap, created = Scrap.objects.get_or_create(user=request.user, post=post)

        if not created:
            scrap.delete()
            return Response({'message': '스크랩이 취소되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '스크랩이 추가되었습니다.'}, status=status.HTTP_201_CREATED)

class CommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent__isnull=True).order_by('-created_at')

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자가 작성한 댓글만 삭제 가능
        return Comment.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
class MyCommentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 내가 쓴 댓글들의 post_id 추출
        user_comments = Comment.objects.filter(user=request.user).values_list('post_id', flat=True)

        # 중복 제거된 post만 조회  
        posts = Post.objects.filter(id__in=set(user_comments)).order_by('-created_at')

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
