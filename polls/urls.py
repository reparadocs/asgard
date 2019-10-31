from django.urls import path
from . import views

urlpatterns = [
  path('vote', views.SubmitVote.as_view(), name='vote'),
  path('status', views.GetStatus.as_view(), name='status'),
  path('question', views.SubmitQuestion.as_view(), name='question')
]