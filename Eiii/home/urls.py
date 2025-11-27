from django.urls import path
from .views import HomeView
from communities import views
from .views import ScheduleCreateView, ScheduleListView, ScheduleDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),
    path('schedule/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-delete'),
    # path('event/', views.recommend, name='recommend'),
]