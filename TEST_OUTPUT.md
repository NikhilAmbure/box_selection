# Test Output

## 1. Automated Tests

The project includes automated tests covering the packing algorithm, box selection, API behavior, and related functionality.

### Command

```bash
python manage.py test packing
```

### Result

```text
# Test output

```
Found 19 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, packing, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying packing.0001_initial... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_no_box_fits_returns_422 (packing.tests.ApiTests.test_no_box_fits_returns_422) ... ok
test_order_endpoint (packing.tests.ApiTests.test_order_endpoint) ... ok
test_order_not_found_and_empty (packing.tests.ApiTests.test_order_not_found_and_empty) ... ok
test_payload_bad_body (packing.tests.ApiTests.test_payload_bad_body) ... ok
test_payload_bad_quantity (packing.tests.ApiTests.test_payload_bad_quantity) ... ok
test_payload_success (packing.tests.ApiTests.test_payload_success) ... ok
test_payload_unknown_sku (packing.tests.ApiTests.test_payload_unknown_sku) ... ok
test_item_too_big (packing.tests.PackerTests.test_item_too_big) ... ok
test_single_item_fits_exactly (packing.tests.PackerTests.test_single_item_fits_exactly) ... ok
test_single_item_needs_rotation (packing.tests.PackerTests.test_single_item_needs_rotation) ... ok
test_two_items_side_by_side (packing.tests.PackerTests.test_two_items_side_by_side) ... ok
test_volume_ok_but_geometry_fails (packing.tests.PackerTests.test_volume_ok_but_geometry_fails) ... ok
test_empty_order_rejected (packing.tests.RecommendTests.test_empty_order_rejected) ... ok
test_no_box_fits (packing.tests.RecommendTests.test_no_box_fits) ... ok
test_overweight_everywhere (packing.tests.RecommendTests.test_overweight_everywhere) ... ok
test_picks_cheapest_fitting (packing.tests.RecommendTests.test_picks_cheapest_fitting) ... ok
test_quantity_forces_bigger_box (packing.tests.RecommendTests.test_quantity_forces_bigger_box) ... ok
test_tie_on_cost_prefers_smaller_volume (packing.tests.RecommendTests.test_tie_on_cost_prefers_smaller_volume) ... ok
test_weight_forces_bigger_box (packing.tests.RecommendTests.test_weight_forces_bigger_box) ... ok

----------------------------------------------------------------------
Ran 19 tests in 0.018s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```

```

---

## 2. Manual API Tests

The recommendation API was manually tested using Postman.

### Test 1 — Book × 1

**Request**

```http
POST /api/recommend-box/
```

```json
{
    "items": [
        {
            "sku": "BK1",
            "quantity": 1
        }
    ]
}
```

**Result**

```json
{
    "recommended_box": {
        "id": 1,
        "name": "Small",
        "cost": "10.00"
    },
    "alternatives": [
        {
            "id": 2,
            "name": "Medium",
            "cost": "20.00"
        },
        {
            "id": 3,
            "name": "Large",
            "cost": "35.00"
        }
    ],
    "total_weight": 0.5,
    "unit_count": 1
}
```

**Result:** PASS

---

### Test 2 — Shoe × 1

**Request**

```http
POST /api/recommend-box/
```

```json
{
    "items": [
        {
            "sku": "SHOE1",
            "quantity": 1
        }
    ]
}
```

**Result**

```json
{
    "recommended_box": {
        "id": 2,
        "name": "Medium",
        "cost": "20.00"
    },
    "alternatives": [
        {
            "id": 3,
            "name": "Large",
            "cost": "35.00"
        }
    ],
    "total_weight": 1.2,
    "unit_count": 1
}
```

**Result:** PASS

---

### Test 3 — TV × 1

**Request**

```http
POST /api/recommend-box/
```

```json
{
    "items": [
        {
            "sku": "TV1",
            "quantity": 1
        }
    ]
}
```

**Result**

```json
{
    "error": "No single box can hold this order."
}
```

**Result:** PASS

The TV dimensions exceed the available box dimensions, so no suitable box is returned.

---

### Test 4 — Book + Shoe

**Request**

```http
POST /api/recommend-box/
```

```json
{
    "items": [
        {
            "sku": "BK1",
            "quantity": 1
        },
        {
            "sku": "SHOE1",
            "quantity": 1
        }
    ]
}
```

**Result**

```json
{
    "recommended_box": {
        "id": 2,
        "name": "Medium",
        "cost": "20.00"
    },
    "alternatives": [
        {
            "id": 3,
            "name": "Large",
            "cost": "35.00"
        }
    ],
    "total_weight": 1.7,
    "unit_count": 2
}
```

**Result:** PASS

---

### Test 5 — Book × 3

**Request**

```http
POST /api/recommend-box/
```

```json
{
    "items": [
        {
            "sku": "BK1",
            "quantity": 3
        }
    ]
}
```

**Result**

```json
{
    "recommended_box": {
        "id": 1,
        "name": "Small",
        "cost": "10.00"
    },
    "alternatives": [
        {
            "id": 2,
            "name": "Medium",
            "cost": "20.00"
        },
        {
            "id": 3,
            "name": "Large",
            "cost": "35.00"
        }
    ],
    "total_weight": 1.5,
    "unit_count": 3
}
```

**Result:** PASS

This test verifies that product quantity is expanded into multiple physical items before packing.

---

### Test 6 — Existing Order

An existing order containing the Book and Shoe products was tested using the order recommendation endpoint.

**Request**

```http
GET /api/orders/ORD-001/recommend-box/
```

**Result**

```json
{
    "recommended_box": {
        "id": 2,
        "name": "Medium",
        "cost": "20.00"
    },
    "alternatives": [
        {
            "id": 3,
            "name": "Large",
            "cost": "35.00"
        }
    ],
    "total_weight": 1.7,
    "unit_count": 2
}
```

**Result:** PASS

---

## 3. Manual Test Summary

| Test Case                | Expected Result | Result |
| ------------------------ | --------------- | ------ |
| Book × 1                 | Small box       | PASS   |
| Shoe × 1                 | Medium box      | PASS   |
| TV × 1                   | No suitable box | PASS   |
| Book + Shoe              | Medium box      | PASS   |
| Book × 3                 | Small box       | PASS   |
| Existing order `ORD-001` | Medium box      | PASS   |

## 4. Notes

The manual API tests were performed using the seeded demo data:

### Boxes

| Box    | Dimensions   | Max Weight |  Cost |
| ------ | ------------ | ---------: | ----: |
| Small  | 20 × 15 × 10 |       5 kg | 10.00 |
| Medium | 40 × 30 × 20 |      15 kg | 20.00 |
| Large  | 80 × 60 × 40 |      30 kg | 35.00 |

### Products

| SKU   | Product  |    Dimensions | Weight |
| ----- | -------- | ------------: | -----: |
| BK1   | Book     |   20 × 14 × 3 | 0.5 kg |
| SHOE1 | Shoe box |  33 × 20 × 12 | 1.2 kg |
| TV1   | TV       | 100 × 60 × 10 |   8 kg |
