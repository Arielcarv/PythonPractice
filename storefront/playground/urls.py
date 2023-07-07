from django.urls import path
from playground.views import celery_email_sender, email_sender, home, say, simulate_delay


urlpatterns = [
    path("", home, name="home"),
    path("hello/", say, name="hello"),
    path("send/", email_sender, name="send"),
    path("celery/send/", celery_email_sender, name="celery-send"),
    path("simulation/", simulate_delay, name="simulate-delay"),
]
