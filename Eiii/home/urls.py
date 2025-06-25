from django.urls import path
from .views import HomeView
from communities import views

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    # path('event/', views.recommend, name='recommend'),
]