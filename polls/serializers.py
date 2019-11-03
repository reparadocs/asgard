from rest_framework import serializers
from .models import *
from django.core.exceptions import ObjectDoesNotExist


class VoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vote
    exclude = ('id',)
  
class OptionSerializer(serializers.ModelSerializer):
  votes = serializers.IntegerField()

  class Meta:
    model = Option
    exclude = ()

class QuestionSerializer(serializers.ModelSerializer):
  option_set = OptionSerializer(many=True)

  class Meta:
    model = Question
    exclude = ('id',)

class SubmitQuestionSerializer(serializers.Serializer):
  question = serializers.CharField(max_length=500)
  options = serializers.ListField(child=serializers.CharField(max_length=100))