from django.urls import path
from playground.views import (
    celery_email_sender,
    email_sender,
    home,
    say,
    simulate_delay,
    simulate_delay_caching,
)


urlpatterns = [
    path("", home, name="home"),
    path("hello/", say, name="hello"),
    path("send/", email_sender, name="send"),
    path("celery/send/", celery_email_sender, name="celery-send"),
    path("simulation/", simulate_delay, name="simulate-delay"),
    path("caching/", simulate_delay_caching, name="simulate-delay-caching"),
]
