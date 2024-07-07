from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.
class Question(models.Model):
    """
    model for questions
    """
    question = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Question"

class Answer(models.Model):
    """
    model for answers
    For single question add multiple answers
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return self.answer
    
    class Meta:
        verbose_name_plural = "Answer"

class Vote(models.Model):
    """
    model for vote
    whenever a user click a vote,  answer and user id are stored in this model
    And we can add conditions according to requirements like
    if user can vote multiple answer to same question
    or 
    if user can vote only one of the answer to the question
    by querying  this model that the user have voted for 
    the particular question or not.
        if voted_for_this_question
            return not allowed to vote
        if not
            return allow to vote
    
    
    both condtion can be fulfilled by this model

    """
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        """
        this save if for condition second where if a user can vote for only one of the
        answer of the  question
        """
        get_vote_data = Vote.objects.filter(user=self.user)
        get_answer_data = Answer.objects.filter(answer=self.answer)
        get_question = [str(obj.question.id) for obj in get_answer_data]
        get_question = get_question[0]
        get_all_answer_of_related_question = Answer.objects.filter(question=get_question)
        for obj in get_all_answer_of_related_question:
            for obj1 in get_vote_data:

                if str(obj.answer) == str(obj1.answer):
                    raise ValidationError("already answered")
                else:
                    print("false")
            
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Vote"

    