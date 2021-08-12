from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    questions_answered = models.IntegerField()
    correctly_answered = models.IntegerField()
    wrongly_answered = models.IntegerField()
    quiz_date_time = models.DateTimeField(auto_now_add=True)
    correct_answer = models.CharField(max_length=100000000,default=None,null=True,blank=True)
    question = models.CharField(max_length=100000000,default=None,null=True,blank=True)
    quiz_cat = models.CharField(max_length=100000000,default=None,null=True,blank=True)
    ques_count = models.IntegerField(null=True,blank=True)

