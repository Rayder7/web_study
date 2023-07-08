from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from utils import make_excel


@shared_task(name="dummy_task")
def dummy_task():
    pass


@shared_task(name="Excel")
def make_excel_task():
    make_excel()