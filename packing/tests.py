from decimal import Decimal

from django.test import TestCase

from .models import Box, Order, OrderItem, Product
from .services import BoxSpec, Item, NoSuitableBox, can_pack, recommend_box


def spec(id, name, l, w, h, mw, cost):
    return BoxSpec(id, name, l, w, h, mw, Decimal(cost))


SMALL = spec(1, "Small", 20, 15, 10, 5, "10")
MED = spec(2, "Medium", 40, 30, 20, 15, "20")
LARGE = spec(3, "Large", 80, 60, 40, 30, "35")


class PackerTests(TestCase):
    def test_single_item_fits_exactly(self):
        self.assertTrue(can_pack([Item(20, 15, 10, 1)], (20, 15, 10)))

    def test_single_item_needs_rotation(self):
        self.assertTrue(can_pack([Item(10, 15, 20, 1)], (20, 15, 10)))

    def test_item_too_big(self):
        self.assertFalse(can_pack([Item(21, 1, 1, 1)], (20, 15, 10)))

    def test_two_items_side_by_side(self):
        self.assertTrue(can_pack([Item(10, 15, 10, 1)] * 2, (20, 15, 10)))

    def test_volume_ok_but_geometry_fails(self):
        # Two 6x6x6 cubes (432 vol) inside 10x10x5 (500 vol): volume passes, geometry can't.
        self.assertFalse(can_pack([Item(6, 6, 6, 1)] * 2, (10, 10, 5)))


class RecommendTests(TestCase):
    def test_picks_cheapest_fitting(self):
        best, alts = recommend_box([Item(5, 5, 5, 1)], [LARGE, MED, SMALL])
        self.assertEqual(best.name, "Small")
        self.assertEqual([b.name for b in alts], ["Medium", "Large"])

    def test_weight_forces_bigger_box(self):
        best, _ = recommend_box([Item(5, 5, 5, 8)], [SMALL, MED, LARGE])
        self.assertEqual(best.name, "Medium")

    def test_quantity_forces_bigger_box(self):
        best, _ = recommend_box([Item(10, 15, 10, 1)] * 3, [SMALL, MED, LARGE])
        self.assertEqual(best.name, "Medium")

    def test_tie_on_cost_prefers_smaller_volume(self):
        a = spec(1, "A", 30, 30, 30, 10, "10")
        b = spec(2, "B", 20, 20, 20, 10, "10")
        best, _ = recommend_box([Item(5, 5, 5, 1)], [a, b])
        self.assertEqual(best.name, "B")

    def test_no_box_fits(self):
        with self.assertRaises(NoSuitableBox):
            recommend_box([Item(100, 100, 100, 1)], [SMALL, MED, LARGE])

    def test_overweight_everywhere(self):
        with self.assertRaises(NoSuitableBox):
            recommend_box([Item(1, 1, 1, 99)], [SMALL, MED, LARGE])

    def test_empty_order_rejected(self):
        with self.assertRaises(ValueError):
            recommend_box([], [SMALL])


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Box.objects.create(name="Small", length=20, width=15, height=10, max_weight=5, cost="10.00")
        Box.objects.create(name="Medium", length=40, width=30, height=20, max_weight=15, cost="20.00")
        cls.book = Product.objects.create(sku="BK1", name="Book", length=20, width=14, height=3, weight=0.5)
        cls.tv = Product.objects.create(sku="TV1", name="TV", length=100, width=60, height=10, weight=8)

    def post(self, body):
        return self.client.post("/api/recommend-box/", body, content_type="application/json")

    def test_payload_success(self):
        r = self.post({"items": [{"sku": "BK1", "quantity": 2}]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["recommended_box"]["name"], "Small")

    def test_payload_unknown_sku(self):
        self.assertEqual(self.post({"items": [{"sku": "NOPE"}]}).status_code, 404)

    def test_payload_bad_quantity(self):
        self.assertEqual(self.post({"items": [{"sku": "BK1", "quantity": 0}]}).status_code, 400)

    def test_payload_bad_body(self):
        self.assertEqual(self.post({"foo": 1}).status_code, 400)
        r = self.client.post("/api/recommend-box/", "not json", content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_no_box_fits_returns_422(self):
        self.assertEqual(self.post({"items": [{"sku": "TV1"}]}).status_code, 422)

    def test_order_endpoint(self):
        order = Order.objects.create(reference="ORD-1")
        OrderItem.objects.create(order=order, product=self.book, quantity=1)
        r = self.client.get("/api/orders/ORD-1/recommend-box/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["recommended_box"]["name"], "Small")

    def test_order_not_found_and_empty(self):
        self.assertEqual(self.client.get("/api/orders/X/recommend-box/").status_code, 404)
        Order.objects.create(reference="EMPTY")
        self.assertEqual(self.client.get("/api/orders/EMPTY/recommend-box/").status_code, 400)
