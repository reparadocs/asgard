from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

class SubmitVote(APIView):
  def post(self, request, format=None):
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
      if Vote.objects.filter(user_id=serializer.validated_data['user_id'], chosen__question=serializer.validated_data['chosen'].question).count() > 0:
        return Response("Duplicate vote", status=status.HTTP_400_BAD_REQUEST)
      else:
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStatus(APIView):
  def get(self, request, format=None):
    now = timezone.now()
    delta = timedelta(seconds=30)
    question = Question.objects.order_by('-time').first()
    if question:
      status_info = {'status': 'results'}
      if (question.time + delta) > now:
        status_info = {'status': 'question'}

      serializer = QuestionSerializer(question)
      status_info.update(serializer.data)
      return Response(status_info)
    else:
      return Response({'status': 'null'})

class SubmitQuestion(APIView):
  def post(self, request, format=None):
    serializer = SubmitQuestionSerializer(data=request.data)
    if serializer.is_valid():
      q = Question(text=serializer.validated_data['question'])
      q.save()
      for option in serializer.validated_data['options']:
        o = Option(text=option, question=q)
        o.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView(APIView):
  def get(self, request, format=None):
    comments = Comment.objects.order_by('-id')[:20]
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
