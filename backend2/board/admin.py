from django.contrib import admin
from broadcast.models import Broadcast
from message.models import Message
from questions.models import Question, UserQuestionRecord, QuestionBank
from users.models import User

admin.site.register(Broadcast)
admin.site.register(Message)
admin.site.register(QuestionBank)
admin.site.register(Question)
admin.site.register(UserQuestionRecord)
admin.site.register(User)