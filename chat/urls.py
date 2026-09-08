from django.urls import path
from .views import RegisterView,LoginView,RoomView
urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name='login'),
    path('rooms/',RoomView.as_view(),name='room'),
    path('rooms/<int:id>/',RoomView.as_view()),

]


