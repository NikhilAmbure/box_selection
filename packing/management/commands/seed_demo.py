from django.core.management.base import BaseCommand

from packing.models import Box, Product


class Command(BaseCommand):
    help = "Load demo boxes and products"

    def handle(self, *args, **opts):
        for n, l, w, h, mw, c in [("Small", 20, 15, 10, 5, "10.00"), ("Medium", 40, 30, 20, 15, "20.00"),
                                  ("Large", 80, 60, 40, 30, "35.00")]:
            Box.objects.update_or_create(name=n, defaults=dict(length=l, width=w, height=h, max_weight=mw, cost=c))
        for s, n, l, w, h, wt in [("BK1", "Book", 20, 14, 3, 0.5), ("SHOE1", "Shoe box", 33, 20, 12, 1.2),
                                  ("TV1", "TV", 100, 60, 10, 8)]:
            Product.objects.update_or_create(sku=s, defaults=dict(name=n, length=l, width=w, height=h, weight=wt))
        self.stdout.write(self.style.SUCCESS("Seeded demo data."))
