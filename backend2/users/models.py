from django.db import models
from utils.models import MyModel


# Create your models here.

class User(MyModel):
    student_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    password_digest = models.CharField(max_length=255)
    mail = models.EmailField()
    college = models.CharField(max_length=255)
    entryYear = models.CharField(max_length=20)
    avatar = models.CharField(max_length=255)
    user_role = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'


class BlackList(MyModel):
    token = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'black_list'
