import djoser.serializers
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from api.models import (Student, Curator, StudyGroup,
                        StudyGroupStudents, Discipline,
                        FieldStudy, FieldStudyDisciplines)

User = get_user_model()


class UserSerializer(djoser.serializers.UserSerializer):
    """ Сериализатор пользователя """
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'balance')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'balance')


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "first_name", "last_name",
                  "sur_name", "sex", "course")
        model = Student


class CuratorSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "first_name", "last_name", "field_study")
        model = Curator


class StudyGroupSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    free_place_group_count = serializers.SerializerMethodField()
    man_count = serializers.SerializerMethodField()
    woman_count = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "course", "number", "students",
                  "students_count", "free_place_group_count",
                  "man_count", "woman_count")
        model = StudyGroup
    
    def get_students_count(self, obj):
        return obj.students.count()
    
    def get_free_place_group_count(self, obj):
        max_lenth = 20
        count = obj.students.count()
        return max_lenth - count
    
    def get_man_count(self, obj):
        return obj.students.filter(sex="MAN")
    
    def get_woman_count(self, obj):
        return obj.students.filter(sex="WOMAN")
    
    def validate(self, data):
        count = data['students_count']
        if count > 20:
            raise serializers.ValidationError(
                'В группе не больше 20 человек.'
            )
        return data


class StudyGroupStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "study_group", "student")
        model = StudyGroupStudents
    

class DisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "name", "field_study")
        model = Discipline


class FieldStudySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "name", "disciplines", "curator")
        model = FieldStudy


class FieldStudyDisciplinesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "field_study", "discipline")
        model = FieldStudyDisciplines