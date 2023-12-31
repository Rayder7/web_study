# Generated by Django 3.2 on 2023-07-10 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20230710_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldstudy',
            name='disciplines',
            field=models.ManyToManyField(blank=True, null=True, related_name='fieldstudies', to='api.Discipline', verbose_name='Учебная дисциплина'),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='studygroups', to='api.Student', verbose_name='Студенты'),
        ),
    ]
