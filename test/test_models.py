import pytest
from web_study.api.models import Student
from fixtures import student


def test_filter_student(student):
    assert Student.objects.filter(first_name="Пупкин").exists()

def test_update_student(student):
    student.first_name = "Непупкин"
    student.save()
    student_from_db = Student.objects.get(name="Непупкин")
    assert student_from_db.first_name == "Пупкин"