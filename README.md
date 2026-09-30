# AI-Assisted Box Selection System (Django)

Recommends the cheapest shipping box that can hold an order, respecting item dimensions,
box internal dimensions, weight capacity and cost.

## Setup
```bash
python -m venv .venv && .venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo          # demo boxes + products
python manage.py runserver
python manage.py test               # run tests
```

## API
**POST `/api/recommend-box/`**
```json
{"items": [{"sku": "BK1", "quantity": 2}, {"sku": "SHOE1", "quantity": 1}]}
```
**GET `/api/orders/<reference>/recommend-box/`** – uses items of a stored Order (create via `/admin/`).

Response `200`:
```json
{"recommended_box": {"id": 1, "name": "Small", "cost": "10.00"},
 "alternatives": [{"id": 2, "name": "Medium", "cost": "20.00"}],
 "total_weight": 1.0, "unit_count": 2}
```
Errors: `400` bad input, `404` unknown SKU/order, `422` no single box fits.

## Design decisions
- Units: cm and kg. Box dimensions are *internal*.
- Each unit of quantity is expanded into its own item.
- A box is valid if: total weight <= max weight, total item volume <= box volume, and a
  3D guillotine packing heuristic (all 6 rotations) places every item (`packing/services.py`).
- Choice rule: cheapest valid box; ties -> smaller volume -> name.
- Packing logic is pure Python (no DB), so it is unit-tested in isolation; views are thin.

## Known limitations
- Heuristic packer: a "fits" result is always a valid packing, but it may miss a tight
  packing that exists (could recommend a larger box than strictly necessary).
- No padding/void-fill, fragility, or "keep upright" constraints; no multi-box splitting
  (returns 422 if nothing fits). The API has no authentication (assignment scope).
st
- 
## Tests
`packing/tests.py`: packer geometry (rotation, exact fit, volume-passes-but-geometry-fails),
selection rules (cheapest, weight, quantity, tie-break, no fit, empty), and API status codes.
Output in `TEST_OUTPUT.md`; CI in `.github/workflows/tests.yml`.
