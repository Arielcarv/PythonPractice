from django.urls import path
from playground.views import (
    CachingView,
    celery_email_sender,
    email_sender,
    home,
    say,
    simulate_delay,
    simulate_delay_caching,
    simulate_delay_caching_with_decorator,
)


urlpatterns = [
    path("", home, name="home"),
    path("hello/", say, name="hello"),
    path("send/", email_sender, name="send"),
    path("celery/send/", celery_email_sender, name="celery-send"),
    path("simulation/", simulate_delay, name="simulate-delay"),
    path("caching/", simulate_delay_caching, name="simulate-delay-caching"),
    path(
        "caching/decorator",
        simulate_delay_caching_with_decorator,
        name="simulate-delay-caching-with-decorator",
    ),
    path("caching/class", CachingView.as_view(), name="caching-with-class"),
]
