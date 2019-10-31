from django.db import models

class Question(models.Model):
  text = models.CharField(max_length=500)
  time = models.DateTimeField(auto_now_add=True)

class Option(models.Model):
  text = models.CharField(max_length=100)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)

  @property
  def votes(self):
    return self.vote_set.count()

class Vote(models.Model):
  chosen = models.ForeignKey(Option, on_delete=models.CASCADE)
  user_id = models.CharField(max_length=100)
