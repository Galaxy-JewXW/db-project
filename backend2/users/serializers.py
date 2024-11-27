from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'password_digest', 'mail', 'college', 'entryYear', 'avatar', 'user_role']
