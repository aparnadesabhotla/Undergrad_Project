from django.db import models as db_models
from django.contrib.auth import models as auth_models


class Question(db_models.Model):
    author = db_models.ForeignKey(auth_models.User, on_delete=db_models.CASCADE)

    title = db_models.CharField(max_length=200)
    body = db_models.TextField()
    published = db_models.DateTimeField(auto_now_add=True)
    updated = db_models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(db_models.Model):
    author = db_models.ForeignKey(auth_models.User, on_delete=db_models.CASCADE)
    question = db_models.ForeignKey(Question, on_delete=db_models.CASCADE)

    body = db_models.TextField()
    published = db_models.DateTimeField(auto_now_add=True)
    updated = db_models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'answer by {self.author}'
