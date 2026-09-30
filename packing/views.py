import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Order, Product
from .services import NoSuitableBox, expand_items, load_boxes, recommend_box


def _respond(pairs):
    items = expand_items(pairs)
    try:
        best, alts = recommend_box(items, load_boxes())
    except NoSuitableBox as exc:
        return JsonResponse({"error": str(exc)}, status=422)
    return JsonResponse({
        "recommended_box": {"id": best.id, "name": best.name, "cost": str(best.cost)},
        "alternatives": [{"id": b.id, "name": b.name, "cost": str(b.cost)} for b in alts],
        "total_weight": round(sum(i.weight for i in items), 3),
        "unit_count": len(items),
    })


@csrf_exempt
@require_http_methods(["POST"])
def recommend_for_payload(request):
    """POST {"items": [{"sku": "ABC", "quantity": 2}, ...]}"""
    try:
        data = json.loads(request.body or b"{}")
        rows = data["items"]
        if not isinstance(rows, list) or not rows:
            raise ValueError
        pairs = []
        for row in rows:
            qty = row.get("quantity", 1)
            if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
                return JsonResponse({"error": "quantity must be a positive integer"}, status=400)
            try:
                pairs.append((Product.objects.get(sku=row["sku"]), qty))
            except Product.DoesNotExist:
                return JsonResponse({"error": f"Unknown sku: {row['sku']}"}, status=404)
    except (ValueError, KeyError, TypeError, AttributeError):
        return JsonResponse({"error": 'Body must be {"items": [{"sku": str, "quantity": int}, ...]}'}, status=400)
    return _respond(pairs)


@require_http_methods(["GET"])
def recommend_for_order(request, reference):
    try:
        order = Order.objects.prefetch_related("items__product").get(reference=reference)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    pairs = [(i.product, i.quantity) for i in order.items.all()]
    if not pairs:
        return JsonResponse({"error": "Order has no items"}, status=400)
    return _respond(pairs)
