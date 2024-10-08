from celery import shared_task
from PersonnelAddressBook.management.commands.fetch_emails import fetch_emails

@shared_task
def fetch_emails_task():
    fetch_emails()# 調用 fetch_emails 函數

