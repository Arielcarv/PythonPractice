from django.dispatch import receiver
from store.signals import order_created


@receiver(order_created)
def on_order_created(sender, **kwrags) -> None:
    print(kwrags["order"])
