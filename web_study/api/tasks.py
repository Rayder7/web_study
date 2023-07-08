from celery import shared_task
#from api.utils import make_excel


@shared_task(name="dummy_task")
def dummy_task():
    pass


""" @shared_task(name="Excel")
def make_excel_task():
    make_excel() """
