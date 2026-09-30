from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations

EPS = 1e-9

@dataclass(frozen=True)
class Item:
    length: float
    width: float
    height: float
    weight: float


@dataclass(frozen=True)
class BoxSpec:
    id: int
    name: str
    length: float
    width: float
    height: float
    max_weight: float
    cost: Decimal

    @property
    def volume(self):
        return self.length * self.width * self.height


class NoSuitableBox(Exception):
    pass


def _rotations(item):
    return set(permutations((item.length, item.width, item.height)))


def can_pack(items, box_dims):
    """Return True if a valid packing of `items` inside `box_dims` was found."""
    spaces = [tuple(box_dims)]  # free spaces as (l, w, h) anchored anywhere
    for item in sorted(items, key=lambda i: i.length * i.width * i.height, reverse=True):
        placed = False
        for idx, (sl, sw, sh) in enumerate(spaces):
            for (l, w, h) in sorted(_rotations(item)):
                if l <= sl + EPS and w <= sw + EPS and h <= sh + EPS:
                    spaces.pop(idx)
                    # guillotine split into three non-overlapping spaces
                    spaces.extend([
                        (sl - l, sw, sh),   # beside in length
                        (l, sw - w, sh),    # beside in width
                        (l, w, sh - h),     # above
                    ])
                    spaces = [s for s in spaces if min(s) > EPS]
                    spaces.sort(key=lambda s: s[0] * s[1] * s[2])  # best-fit: smallest first
                    placed = True
                    break
            if placed:
                break
        if not placed:
            return False
    return True


def box_fits(items, box):
    if not items:
        return True
    if sum(i.weight for i in items) > box.max_weight + EPS:
        return False
    if sum(i.length * i.width * i.height for i in items) > box.volume + EPS:
        return False
    return can_pack(items, (box.length, box.width, box.height))


def recommend_box(items, boxes):
    """Pure function: returns (BoxSpec, alternatives_list). Raises NoSuitableBox."""
    if not items:
        raise ValueError("Order has no items.")
    fitting = [b for b in boxes if box_fits(items, b)]
    if not fitting:
        raise NoSuitableBox("No single box can hold this order.")
    fitting.sort(key=lambda b: (b.cost, b.volume, b.name))
    return fitting[0], fitting[1:]


def expand_items(pairs):
    """[(Product, qty), ...] -> flat list of Item, one per unit."""
    out = []
    for product, qty in pairs:
        out.extend([Item(product.length, product.width, product.height, product.weight)] * qty)
    return out


def load_boxes():
    from .models import Box
    return [BoxSpec(b.id, b.name, b.length, b.width, b.height, b.max_weight, b.cost)
            for b in Box.objects.all()]
