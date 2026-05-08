import json
import os
import random
import uuid
from datetime import datetime, timedelta
from typing import List


DB_PATH = os.environ.get("ORDER_DB_PATH", "data/orders.json")

CUSTOMER_NAMES = [
    "홍길동", "김철수", "이영희", "박민준", "최수연",
    "정하늘", "강지훈", "윤서연", "임도현", "한소희",
    "오지훈", "신예은", "백승현", "류미래", "조민서",
]

PRODUCTS = [
    ("노트북",      1_200_000, 2_500_000),
    ("스마트폰",      800_000, 1_500_000),
    ("태블릿",       400_000,   900_000),
    ("키보드",        50_000,   200_000),
    ("마우스",        20_000,    80_000),
    ("모니터",       300_000,   800_000),
    ("이어폰",        30_000,   250_000),
    ("웹캠",          40_000,   120_000),
    ("외장SSD",      100_000,   300_000),
    ("USB 허브",      15_000,    60_000),
    ("노트북 거치대",  30_000,   100_000),
    ("블루투스 스피커", 50_000,  200_000),
    ("USB 허브",      15_000,    60_000),
    ("충전기",        20_000,    80_000),
]

STATUSES = ["pending", "processing", "completed", "cancelled"]
STATUS_WEIGHTS = [0.3, 0.2, 0.4, 0.1]


def _random_date(days_back: int = 30) -> str:
    delta = timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return (datetime.now() - delta).isoformat()


def generate_order() -> dict:
    item_count = random.randint(1, 4)
    selected = random.sample(PRODUCTS, item_count)
    items = []
    for name, min_price, max_price in selected:
        unit_price = round(random.uniform(min_price, max_price) / 1000) * 1000
        quantity = random.randint(1, 3)
        items.append({
            "product_name": name,
            "quantity": quantity,
            "unit_price": unit_price,
        })

    total_price = sum(i["unit_price"] * i["quantity"] for i in items)
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]

    return {
        "id": str(uuid.uuid4())[:8],
        "customer_name": random.choice(CUSTOMER_NAMES),
        "items": items,
        "status": status,
        "created_at": _random_date(),
        "total_price": total_price,
    }


def _load_db() -> List[dict]:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_db(orders: List[dict]) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def generate_and_save(count: int = 10) -> List[dict]:
    existing = _load_db()
    new_orders = [generate_order() for _ in range(count)]
    existing.extend(new_orders)
    _save_db(existing)
    return new_orders


def reset_db() -> None:
    _save_db([])
    print(f"DB 초기화 완료: {DB_PATH}")
