from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget

from api.models import (Student, Curator,
                        StudyGroup, Discipline,
                        FieldStudy,)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'course',
    )
    search_fields = ('last_name',)
    list_filter = ('course',)
    ordering = ('last_name',)
    empty_value_display = '-пусто-'


class CuratorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'field_study',
    )
    search_fields = ('last_name',)
    list_filter = ('field_study',)
    ordering = ('last_name',)
    empty_value_display = '-пусто-'


class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'field_study'
    )
    search_fields = ('name',)
    list_filter = ('field_study',)
    ordering = ('-id',)
    empty_value_display = '-пусто-'


class StudyGroupAdmin(admin.ModelAdmin):
    list_display = (
        'number', 'course', 'students',
        'students_count', 'free_place_group_count',
        'man_count', 'woman_count'
    )
    search_fields = ('number',)
    list_filter = ('number', 'course')
    ordering = ('number',)
    empty_value_display = '-пусто-'


class FieldStudyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'disciplines', 'curator',
    )
    search_fields = ('name',)
    list_filter = ('curator',)
    ordering = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Student, StudentAdmin)
admin.site.register(Curator, CuratorAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)
admin.site.register(FieldStudy, FieldStudyAdmin)


class FieldStudyResource(resources.ModelResource):
    disciplines = Field(
        column_name='disciplines',
        attribute='disciplines',
        widget=ManyToManyWidget(
            Discipline, field='name', separator=','
        )
    )

    class Meta:
        model = FieldStudy
        fields = ("id", "name", "disciplines", "curator",)


class StudyGroupResource(resources.ModelResource):
    Students = Field(
        column_name='students',
        attribute='students',
        widget=ManyToManyWidget(
            Student, field='last_name', separator=','
        )
    )

    class Meta:
        model = StudyGroup
        fields = ('number', 'course', 'students',
                  'students_count', 'free_place_group_count',
                  'man_count', 'woman_count',)
