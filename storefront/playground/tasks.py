from time import sleep
from celery import shared_task


@shared_task
def notify_customers(message):
    print("Sending messages...\n")
    sleep(10)
    print(f"{message}")
    print("Emails were sent successfully")
