from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProfilePreviewSerializer
from rest_framework.generics import RetrieveAPIView


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "유효하지 않은 refresh 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


class MatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            my_profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({"error": "먼저 프로필을 작성해주세요."}, status=400)

        # 나를 제외한 모든 프로필
        candidates = Profile.objects.exclude(user=request.user)

        def calculate_score(p):
            score = 0
            fields = [
                'preferred_gender',
                'dining_style',
                'eating_speed',
                'meal_purpose',
                'dessert'
            ]

            for field in fields:
                my_value = getattr(my_profile, field)
                other_value = getattr(p, field)
                if my_value == '상관없음' or other_value == '상관없음':
                    continue
                if my_value == other_value:
                    score += 1

            # preferred_menu, dietary_restrictions: 교집합 수 비교
            score += len(set(my_profile.preferred_menu) & set(p.preferred_menu))
            score += len(set(my_profile.dietary_restrictions) & set(p.dietary_restrictions))
            return score

        # 미리보기 매칭 후보 정렬 (점수 높은 순)
        sorted_profiles = sorted(candidates, key=calculate_score, reverse=True)

        # 최대 6명까지만 반환 
        top_matches = sorted_profiles[:6]
        serializer = ProfilePreviewSerializer(top_matches, many=True)
        return Response(serializer.data)

class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]