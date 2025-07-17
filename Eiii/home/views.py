from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, permissions
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView



class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        schedules = Schedule.objects.filter(user=user).order_by('date')
        schedule_data = ScheduleSerializer(schedules, many=True).data

        return Response({
            "message": "home",
            "schedules": schedule_data
        }, status=status.HTTP_200_OK
        )
    
class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user).order_by('date')
    

class ScheduleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "일정이 삭제되었습니다."}, status=status.HTTP_200_OK)




