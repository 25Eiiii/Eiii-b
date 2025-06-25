from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "로그인 성공. Home으로 이동했습니다."}, status=status.HTTP_200_OK)
