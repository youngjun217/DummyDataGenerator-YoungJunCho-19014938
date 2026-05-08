import sys
import os
import argparse
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from generator import generate_and_save, reset_db, _load_db, DB_PATH


def _dw(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)

def _ljust(s: str, w: int) -> str:
    return s + " " * max(0, w - _dw(s))

def _rjust(s: str, w: int) -> str:
    return " " * max(0, w - _dw(s)) + s


def main() -> None:
    parser = argparse.ArgumentParser(description="주문 더미 데이터 생성기")
    parser.add_argument("-n", "--count", type=int, default=10, help="생성할 주문 수 (기본값: 10)")
    parser.add_argument("--reset", action="store_true", help="생성 전 DB 초기화")
    parser.add_argument("--list", action="store_true", help="현재 저장된 주문 목록만 출력 (생성 없음)")
    args = parser.parse_args()

    print(f"DB 경로: {DB_PATH}")

    if args.list:
        existing = _load_db()
        print(f"\n현재 저장된 주문: {len(existing)}건")
        print(_ljust("ID", 10) + " " + _ljust("고객명", 15) + " " + _ljust("상태", 12) + "  " + "생성일")
        print("-" * 60)
        for o in existing:
            print(_ljust(o["id"], 10) + " " + _ljust(o["customer_name"], 15) + " " + _ljust(o["status"], 12) + "  " + o["created_at"][:19])
        return

    if args.reset:
        reset_db()

    print(f"더미 주문 {args.count}건 생성 중...")
    new_orders = generate_and_save(args.count)

    print(f"\n생성 완료: {len(new_orders)}건")
    print(
        _ljust("ID", 10) + " " +
        _ljust("고객명", 15) + " " +
        _ljust("상태", 12) + " " +
        _rjust("총액", 14) + "  " +
        "생성일"
    )
    print("-" * 70)
    for o in new_orders:
        print(
            _ljust(o["id"], 10) + " " +
            _ljust(o["customer_name"], 15) + " " +
            _ljust(o["status"], 12) + " " +
            _rjust(f"{o['total_price']:,.0f}원", 14) + "  " +
            o["created_at"][:19]
        )
    from collections import Counter
    status_counts = Counter(o["status"] for o in new_orders)
    print(f"\n[상태별 요약]")
    for status, count in sorted(status_counts.items()):
        print(f"  {status:<12} : {count}건")
    print(f"\norders.json 에 저장되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
