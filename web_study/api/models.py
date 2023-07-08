from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    class Sex(models.TextChoices):
        MAN = "MAN"
        WOMAN = "WOMAN"

    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    sur_name = models.CharField('Отчество', max_length=50)
    sex = models.CharField(
        choises=Sex.choises,
        default=Sex.MAN,
        max_length=5
    )
    course = models.SmallIntegerField('год обучения')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self) -> str:
        return self.username


class StudyGroup(models.Model):
    number = models.IntegerField('Номер группы')
    course = models.SmallIntegerField('год обучения')
    students = models.ManyToManyField(
        Student, through='StudyGroupStudents',
        verbose_name='Студенты',
        related_name='studygroups'
    )

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self) -> str:
        return self.username


class StudyGroupStudents(models.Model):
    study_group = models.ForeignKey(StudyGroup, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f"{self.study_group} + {self.student} "


class Discipline(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )
    field_study = models.ForeignKey(FieldStudy, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Учебная дисциплина'
        verbose_name_plural = 'Учебные дисциплины'

    def __str__(self) -> str:
        return self.name


class FieldStudy(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )
    disciplines = models.ManyToManyField(
        Discipline, through='StudyGroupStudents',
        verbose_name='Учебная дисциплина',
        related_name='fieldstudies'
    )
    curator = models.ForeignKey(Curator, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'


class FieldStudyDisciplines(models.Model):
    field_study = models.ForeignKey(FieldStudy, on_delete = models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f"{self.field_study} + {self.discipline} "


class Curator(User):
    field_study = models.ForeignKey(FieldStudy, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Куратор'
        verbose_name_plural = 'Кураторы'

    def __str__(self) -> str:
        return self.username
