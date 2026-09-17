from django.urls import path
from .views import RegisterView,LoginView,RoomView,MessageView,RoomMemberView


urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name='login'),
    path('rooms/',RoomView.as_view(),name='room'),
    path('rooms/<int:id>/',RoomView.as_view()),
    path("messages/", MessageView.as_view()),
    path('rooms/<int:id>/messages/',MessageView.as_view()),
    path('rooms/<int:id>/members/',RoomMemberView.as_view()),

]


